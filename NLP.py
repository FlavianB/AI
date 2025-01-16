import argparse
import random
import string
from collections import Counter

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from rake_nltk import Rake
import rowordnet as rwn  # <-- Import RoWordNet

# Download necessary NLTK packages (if not already installed)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

from openai import OpenAI

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Initialize RoWordNet globally once, so we don’t reload it repeatedly.
ro_wordnet = rwn.RoWordNet()


def read_text():
    """
    Reads text from a file (if provided via --file) or from stdin.
    """
    parser = argparse.ArgumentParser(description='Process text input.')
    parser.add_argument('--file', type=str, help='Path to the input file.')
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = input("Enter the text: ")

    return text


def detect_language(text):
    """
    Detects the language of the given text using langdetect.
    Returns a two-letter code (e.g., 'en', 'ro') or "Unknown language".
    """
    try:
        language = detect(text)
        return language
    except LangDetectException:
        return "Unknown language"


def is_word(token):
    """
    Checks if the token contains at least one alphabetic character.
    """
    return any(char.isalpha() for char in token)


def stylometric_analysis(text):
    """
    Performs a basic stylometric analysis of the text:
     - Word count
     - Character count
     - Word frequencies
     - Average word length
     - Average sentence length
     - Vocabulary richness
    Returns a dictionary with these metrics.
    """
    text_no_punct = text.translate(str.maketrans('', '', string.punctuation))
    words = nltk.word_tokenize(text_no_punct)
    sentences = nltk.sent_tokenize(text)

    word_count = len(words)
    char_count = len(text)
    word_freq = Counter(words)
    avg_word_length = (sum(len(w) for w in words) / word_count) if word_count else 0
    avg_sentence_length = (word_count / len(sentences)) if sentences else 0
    vocab_richness = (len(set(words)) / word_count) if word_count else 0

    return {
        'word_count': word_count,
        'char_count': char_count,
        'word_freq': word_freq,
        'avg_word_length': avg_word_length,
        'avg_sentence_length': avg_sentence_length,
        'vocab_richness': vocab_richness
    }


# ------------------- ENGLISH WORDNET LOGIC ------------------- #

def get_related_words_english(word):
    """
    Fetch related words for the given English word (synonyms, hypernyms, negated antonyms)
    from NLTK WordNet.
    """
    synonyms = set()
    hypernyms = set()
    negated_antonyms = set()

    synsets = wn.synsets(word)
    if not synsets:
        return synonyms, hypernyms, negated_antonyms

    # Limit to only the first 1-2 synsets for simplicity
    for syn in synsets[:2]:
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
            if lemma.antonyms():
                negated_antonyms.add(f"not_{lemma.antonyms()[0].name()}")
        for hyper in syn.hypernyms():
            for lemma in hyper.lemmas():
                hypernyms.add(lemma.name())

    return synonyms, hypernyms, negated_antonyms


def get_best_replacement_english(word, context):
    """
    Find the best replacement word (for English) using WordNet-based semantic similarity.
    """
    if len(word) <= 3:
        return word

    synonyms, hypernyms, negated_antonyms = get_related_words_english(word)
    candidates = list(synonyms.union(hypernyms, negated_antonyms))

    best_candidate = word
    max_similarity = 0.0

    original_synsets = wn.synsets(word)
    if not original_synsets:
        return word

    # Create a list of synsets for context words (just the first synset of each)
    context_synsets = []
    for ctx_word in context:
        ctx_synsets = wn.synsets(ctx_word)[:1]
        context_synsets.extend(ctx_synsets)

    for candidate in candidates:
        candidate_synsets = wn.synsets(candidate)[:1]
        if not candidate_synsets:
            continue

        for original_synset in original_synsets:
            for candidate_synset in candidate_synsets:
                similarity = (original_synset.wup_similarity(candidate_synset) or 0)

                # Incorporate context similarity
                context_similarity = sum(
                    (candidate_synset.wup_similarity(ctx_synset) or 0)
                    for ctx_synset in context_synsets
                )

                total_similarity = similarity + context_similarity
                if total_similarity > max_similarity:
                    max_similarity = total_similarity
                    best_candidate = candidate

    return f"<{best_candidate}>" if best_candidate != word else word


# ------------------- ROMANIAN WORDNET (ROWORDNET) LOGIC ------------------- #

def get_best_replacement_romanian(word):
    """
    Attempts to replace a Romanian word with another synonym using RoWordNet.
    This is a simple demonstration that:
      - searches for synsets containing the word
      - picks the first synset
      - randomly chooses another literal if available
    """
    # If the word is very short, skip it
    if len(word) <= 2:
        return word

    # Strict search so we don't catch partial strings
    synset_ids = ro_wordnet.synsets(literal=word, strict=True)
    if not synset_ids:
        return word

    # Just pick the first synset for simplicity
    synset_id = synset_ids[0]
    synset_obj = ro_wordnet.synset(synset_id)
    literals = synset_obj.literals  # synonyms in Romanian

    # If there's more than one literal in the synset, try to pick a different one
    candidates = [lit for lit in literals if lit.lower() != word.lower()]

    if not candidates:
        return word

    # Simple random choice from the synonyms
    replacement = random.choice(candidates)
    # Mark replaced words with angle brackets
    return f"<{replacement}>" if replacement != word else word


def replace_words(text, language="en", replacement_rate=1):
    """
    Replace words in the text with:
      - WordNet-based English synonyms (if language = 'en')
      - RoWordNet-based Romanian synonyms (if language = 'ro')
    at the specified replacement rate.
    """
    tokens = word_tokenize(text)
    words = [token for token in tokens if is_word(token)]
    num_replacements = int(replacement_rate * len(words))

    # Choose random positions to replace
    indices_to_replace = random.sample(range(len(words)), num_replacements)

    for i in indices_to_replace:
        # Small context window for English
        context_window = words[max(0, i-2):i] + words[i+1:i+3]

        if language == "en":
            new_word = get_best_replacement_english(words[i], context_window)
        elif language == "ro":
            # For Romanian, we do the simpler approach
            new_word = get_best_replacement_romanian(words[i])
        else:
            new_word = words[i]  # fallback / do nothing for other languages

        words[i] = new_word

    # Rebuild the text from the replaced words
    word_index = 0
    new_tokens = []
    for token in tokens:
        if is_word(token):
            new_tokens.append(words[word_index])
            word_index += 1
        else:
            new_tokens.append(token)

    return TreebankWordDetokenizer().detokenize(new_tokens)


def extract_keywords(text, lang):
    """
    Extracts keywords from text using RAKE.
    """
    rake = Rake(language=lang)
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()


def generate_sentences(keywords, original_text, lang="english"):
    """
    Generates exactly one sentence per keyword that attempts to preserve
    the original sense or context from a given text.

    :param keywords: list of extracted keywords
    :param original_text: the original text from which keywords were extracted
    :param lang: "english", "romanian", etc. (you can adapt prompt accordingly)
    :return: list of sentences
    """

    # 1) Instantiate your client (with your key).
    #    You could also read your key from an environment variable if you prefer.
    api_key = "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"
    client = OpenAI(api_key=api_key)

    # 2) Build your "system" and "user" messages for a ChatCompletion.
    system_message = (
        "You are a helpful assistant. You have been given a text and some keywords. "
        "Your job is to generate exactly one sentence for each keyword, preserving the "
        "text's original sense and context. Write in a clear, coherent style."
    )

    user_message = (
        f"Here is the text:\n\n{original_text}\n\n"
        f"Language: {lang}\n"
        "Please generate one concise sentence for each of the following keywords, "
        "ensuring you preserve the meaning from the text:\n\n"
    )
    for kw in keywords:
        user_message += f"- {kw}\n"

    user_message += (
        "\nRespond with exactly one sentence for each keyword in the same order. "
        "Separate each sentence clearly (e.g., a new line for each)."
    )

    # 3) Create a chat completion request. For GPT-4, use "gpt-4" if you have access.
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        max_tokens=500,
        temperature=0.7,
    )

    # 4) The response is a pydantic model. We get the assistant's text from the first choice.
    generated_text = response.choices[0].message.content.strip()

    # 5) Split lines to map them back to the keywords.
    sentences = [line.strip() for line in generated_text.split("\n") if line.strip()]

    return sentences


def save_analysis_to_file(analysis, filename='stylometric_analysis.txt'):
    """
    Saves stylometric analysis results to a text file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Word count: {analysis['word_count']}\n")
        f.write(f"Character count: {analysis['char_count']}\n")
        f.write(f"Average word length: {analysis['avg_word_length']:.2f}\n")
        f.write(f"Average sentence length (in words): {analysis['avg_sentence_length']:.2f}\n")
        f.write(f"Vocabulary richness (type-token ratio): {analysis['vocab_richness']:.2f}\n\n")

        f.write("Word frequencies:\n")
        for w, freq in analysis['word_freq'].most_common():
            f.write(f"{w}: {freq}\n")


def save_altered_text_to_file(altered_text, filename='altered_text.txt'):
    """
    Saves the altered (replaced) text to a file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(altered_text)


def main():
    # Read text (from file or stdin)
    text = read_text()

    # Detect language (e.g., 'en', 'ro', or something else)
    detected_lang = detect_language(text)
    print(f"Detected language code: {detected_lang}")

    # Normalize the language for RAKE
    # We'll map only 'en' -> 'english' and 'ro' -> 'romanian' for now.
    # Anything else defaults to 'english' in RAKE.
    if detected_lang == "en":
        rake_language = "english"
    elif detected_lang == "ro":
        rake_language = "romanian"
    else:
        rake_language = "english"

    # Perform stylometric analysis
    analysis = stylometric_analysis(text)
    print(f"Word count: {analysis['word_count']}")
    print(f"Character count: {analysis['char_count']}")
    print(f"Average word length: {analysis['avg_word_length']:.2f}")
    print(f"Average sentence length (in words): {analysis['avg_sentence_length']:.2f}")
    print(f"Vocabulary richness (type-token ratio): {analysis['vocab_richness']:.2f}")

    # Save analysis to file
    save_analysis_to_file(analysis)
    print("Stylometric analysis saved to 'stylometric_analysis.txt'.")

    # Replace words
    altered_text = replace_words(text, language=detected_lang)
    save_altered_text_to_file(altered_text)
    print("Altered text saved to 'altered_text.txt'.")

    # Extract keywords and generate sentences
    keywords = extract_keywords(text, rake_language)
    print("Extracted Keywords:")
    for idx, kw in enumerate(keywords, start=1):
        print(f"{idx}. {kw}")
    sentences = generate_sentences(keywords, text, lang=rake_language)
    print("Generated Sentences:")
    for idx, sentence in enumerate(sentences, start=1):
        print(f"{idx}. {sentence}")

if __name__ == "__main__":
    main()
