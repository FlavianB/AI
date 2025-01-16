import os
import json
import openai
import re
import sys
import time
from typing import Optional
from openai import OpenAI

ASSISTANT_NAME = "Constraint Parser"
MODEL_NAME = "gpt-4"
ASSISTANT_INSTRUCTIONS = """
You are an assistant that converts natural language constraints into a structured JSON format for timetable management.

Given a user input expressing constraints, output a JSON object with the following structure:

{
  "constraints": [
    {
      "type": "unavailable_staff_time" | "unavailable_classroom_time" | "preferred_event",
      "name": "Dr. Smith",                  # Required for unavailable_staff_time
      "id": "C2",                           # Required for unavailable_classroom_time
      "unavailability": {                   # Required for unavailable_staff_time and unavailable_classroom_time
        "Monday": ["08:00-10:00"],
        "Tuesday": ["08:00-10:00"]
      },
      "classroom": "C112",                  # Required for preferred_event
      "instructor": "Dr. Johnson",          # Required for preferred_event
      "course": "IP",                       # Required for preferred_event
      "group": "A2",                        # Required for preferred_event
      "event_type": "Lecture",              # Required for preferred_event
      "preferred_time": {                   # Required for preferred_event
        "Wednesday": ["10:00-12:00"]
      },
      "weight": "hard"
    },
    ...
  ]
}

- Each constraint must include the "weight" field set to "hard".
- Output only the JSON. If unsure about the interpretation, respond with: "I'm unsure about the interpretation of the provided constraints."
"""

CONSTRAINTS_FILE = "constraints.json"
ASSISTANT_ID_FILE = "assistant_id.txt"
POLL_INTERVAL = 5  
MAX_POLL_ATTEMPTS = 12 

def initialize_openai() -> OpenAI:
    api_key = "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"
    client = OpenAI(api_key=api_key)
    return client

def read_assistant_id(file_path: str) -> Optional[str]:
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r') as f:
            assistant_id = f.read().strip()
            if assistant_id:
                return assistant_id
            else:
                return None
    except IOError as e:
        print(f"Error reading assistant ID from file: {e}")
        return None

def write_assistant_id(file_path: str, assistant_id: str):
    try:
        with open(file_path, 'w') as f:
            f.write(assistant_id)
        print(f"Assistant ID saved to '{file_path}'.")
    except IOError as e:
        print(f"Error writing assistant ID to file: {e}")

def create_assistant(client: OpenAI) -> Optional[str]:
    try:
        response = client.beta.assistants.create(
            name=ASSISTANT_NAME,
            instructions=ASSISTANT_INSTRUCTIONS,
            model=MODEL_NAME
        )
        assistant_id = response.id
        if not assistant_id:
            print("Error: Failed to create assistant. No ID returned.")
            return None
        print(f"Assistant '{ASSISTANT_NAME}' created with ID: {assistant_id}")
        return assistant_id
    except openai.OpenAIError as e:
        print(f"OpenAI API error during assistant creation: {e}")
        return None

def get_user_input() -> str:
    print("Enter your constraint in natural language (or type 'exit' to quit):")
    user_input = input("> ")
    return user_input.strip()

def validate_constraints_json(json_data: dict) -> bool:
    if "constraints" not in json_data:
        return False
    if not isinstance(json_data["constraints"], list):
        return False
    for constraint in json_data["constraints"]:
        if "type" not in constraint or "weight" not in constraint:
            return False
        if constraint["weight"] != "hard":
            return False
    return True

def parse_assistant_response(response_text) -> Optional[dict]:
    try:
        response_text = response_text[0].text.value
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            return None
        json_str = json_match.group()
        json_data = json.loads(json_str)
        if validate_constraints_json(json_data):
            return json_data
        else:
            return None
    except json.JSONDecodeError:
        return None

def save_constraints(json_data: dict):
    try:
        if os.path.exists(CONSTRAINTS_FILE):
            with open(CONSTRAINTS_FILE, 'r') as f:
                existing_data = json.load(f)
            existing_constraints = existing_data.get("constraints", [])
            new_constraints = json_data.get("constraints", [])
            merged_constraints = existing_constraints + new_constraints
            json_data["constraints"] = merged_constraints
        with open(CONSTRAINTS_FILE, 'w') as f:
            json.dump(json_data, f, indent=2)
        print(f"Constraints saved to '{CONSTRAINTS_FILE}'.")
    except IOError as e:
        print(f"Error saving constraints to file: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing existing constraints file: {e}")

def get_assistant_response(client: OpenAI, thread_id: str) -> Optional[str]:
    try:
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_message = None
        for msg in messages.data:
            if msg.role == "assistant":
                assistant_message = msg.content
                break
        return assistant_message
    except openai.OpenAIError as e:
        print(f"OpenAI API error while retrieving messages: {e}")
        return None

def check_run_status(client: OpenAI, run_id: str, thread_id: str) -> Optional[str]:
    try:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        status = run.status
        return status
    except openai.OpenAIError as e:
        print(f"OpenAI API error while checking run status: {e}")
        return None

def main():
    client = initialize_openai()
    
    assistant_id = read_assistant_id(ASSISTANT_ID_FILE)
    if assistant_id:
        print(f"Using existing assistant with ID: {assistant_id}")
    else:
        assistant_id = create_assistant(client)
        if not assistant_id:
            sys.exit(1)
        write_assistant_id(ASSISTANT_ID_FILE, assistant_id)
    
    while True:
        user_input = get_user_input()
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        if not user_input:
            print("No input detected. Please enter a valid constraint.")
            continue
        
        try:
            thread = client.beta.threads.create()
            thread_id = thread.id
            if not thread_id:
                print("Error: Failed to create thread.")
                continue
            print(f"Thread created with ID: {thread_id}")
            
            message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=user_input
            )
            print("User message added to thread.")
            
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            run_id = run.id
            if not run_id:
                print("Error: Failed to create run. No Run ID returned.")
                continue
            print(f"Run created with ID: {run_id}")
            
            print("Waiting for assistant response...")
            attempt = 0
            assistant_message = None
            while attempt < MAX_POLL_ATTEMPTS:
                status = check_run_status(client, run_id, thread_id)
                if not status:
                    print("Unable to retrieve run status.")
                    break
                print(f"Run status: {status}")
                if status == "completed":
                    assistant_message = get_assistant_response(client, thread_id)
                    break
                elif status == "failed":
                    print("Run failed.")
                    break
                else:
                    time.sleep(POLL_INTERVAL)
                    attempt += 1
            else:
                print("Run did not complete within the expected time.")
            
            if not assistant_message:
                print("Error: No response from assistant.")
                continue
            
            constraints_json = parse_assistant_response(assistant_message)
            if constraints_json:
                save_constraints(constraints_json)
            else:
                print("I'm unsure about the interpretation of the provided constraints.")
        
        except openai.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            continue

if __name__ == "__main__":
    main()
