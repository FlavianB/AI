import argparse
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import nltk
from collections import Counter
import string
from nltk.corpus import wordnet as wn
import random
from rake_nltk import Rake
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

def is_word(token):
    return any(char.isalpha() for char in token)

def read_text():
    parser = argparse.ArgumentParser(description='Process text input.')
    parser.add_argument('--file', type=str, help='Path to the input file.')
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = input("Enter the text: ")

    return text

text = read_text()

# Ensure consistent results
DetectorFactory.seed = 0

def detect_language(text):
    try:
        language = detect(text)
        return language
    except LangDetectException:
        return "Unknown language"

language = detect_language(text)
print(f"The language of the text is: {language}")

def stylometric_analysis(text):
    # Remove punctuation
    text_no_punct = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize text into words
    words = nltk.word_tokenize(text_no_punct)
    # Tokenize text into sentences
    sentences = nltk.sent_tokenize(text)
    # Count words and characters
    word_count = len(words)
    char_count = len(text)
    # Calculate word frequency
    word_freq = Counter(words)
    # Calculate average word length
    avg_word_length = sum(len(word) for word in words) / word_count if word_count else 0
    # Calculate average sentence length in words
    avg_sentence_length = word_count / len(sentences) if sentences else 0
    # Calculate vocabulary richness (type-token ratio)
    vocab_richness = len(set(words)) / word_count if word_count else 0

    return {
        'word_count': word_count,
        'char_count': char_count,
        'word_freq': word_freq,
        'avg_word_length': avg_word_length,
        'avg_sentence_length': avg_sentence_length,
        'vocab_richness': vocab_richness
    }

import random
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, TreebankWordDetokenizer

def is_word(token):
    # Utility function to check if a token is a word
    return token.isalpha()

def get_related_words(word):
    """
    Fetch related words for the given word, including synonyms, hypernyms, and negated antonyms.
    """
    synonyms = set()
    hypernyms = set()
    negated_antonyms = set()

    synsets = wn.synsets(word)
    if not synsets:
        return synonyms, hypernyms, negated_antonyms  # Return empty sets if no synsets found

    for syn in synsets:
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
            if lemma.antonyms():
                negated_antonyms.add(f"not_{lemma.antonyms()[0].name()}")
        for hyper in syn.hypernyms():
            for lemma in hyper.lemmas():
                hypernyms.add(lemma.name())

    return synonyms, hypernyms, negated_antonyms

def get_best_replacement(word, context):
    """
    Find the best replacement word based on semantic similarity and context.
    """
    synonyms, hypernyms, negated_antonyms = get_related_words(word)
    candidates = list(synonyms.union(hypernyms).union(negated_antonyms))

    # Limit the number of candidates to avoid excessive computation
    # max_candidates = 10
    # candidates = candidates[:max_candidates]

    best_candidate = word
    max_similarity = 0.0

    original_synsets = wn.synsets(word)
    if not original_synsets:
        return word  # Return original word if no synsets are found

    # Extract context words' synsets
    context_synsets = []
    for ctx_word in context:
        ctx_synsets = wn.synsets(ctx_word)
        context_synsets.extend(ctx_synsets)

    for candidate in candidates:
        candidate_synsets = wn.synsets(candidate)
        if not candidate_synsets:
            continue  # Skip candidates with no synsets

        for original_synset in original_synsets:
            for candidate_synset in candidate_synsets:
                similarity = original_synset.wup_similarity(candidate_synset)

                # Incorporate context similarity
                context_similarity = sum((candidate_synset.wup_similarity(ctx_synset) or 0) for ctx_synset in context_synsets)
                total_similarity = similarity + context_similarity

                if total_similarity and total_similarity > max_similarity:
                    max_similarity = total_similarity
                    best_candidate = candidate

    return f"<{best_candidate}>" if best_candidate != word else word

def replace_words(text, replacement_rate=0.5):
    """
    Replace words in the text with their best replacements based on semantic similarity.
    """
    tokens = word_tokenize(text)
    words = [token for token in tokens if is_word(token)]
    num_replacements = int(replacement_rate * len(words))
    indices_to_replace = random.sample(range(len(words)), num_replacements)

    for i in indices_to_replace:
        context_window = words[max(0, i-2):i] + words[i+1:i+3]
        replacement = get_best_replacement(words[i], context_window)
        if replacement:
            words[i] = replacement

    # Reconstruct the text with replacements
    word_index = 0
    new_tokens = []
    for token in tokens:
        if is_word(token):
            new_tokens.append(words[word_index])
            word_index += 1
        else:
            new_tokens.append(token)

    return TreebankWordDetokenizer().detokenize(new_tokens)

def extract_keywords(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()

def generate_sentences(keywords):
    sentences = []
    for keyword in keywords:
        sentence = f"The keyword '{keyword}' is significant in the given context."
        sentences.append(sentence)
    return sentences

def save_analysis_to_file(analysis, filename='stylometric_analysis.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Word count: {analysis['word_count']}\n")
        f.write(f"Character count: {analysis['char_count']}\n")
        f.write(f"Average word length: {analysis['avg_word_length']:.2f}\n")
        f.write(f"Average sentence length (in words): {analysis['avg_sentence_length']:.2f}\n")
        f.write(f"Vocabulary richness (type-token ratio): {analysis['vocab_richness']:.2f}\n")
        f.write("\nWord frequencies:\n")
        for word, freq in analysis['word_freq'].most_common():
            f.write(f"{word}: {freq}\n")

def save_altered_text_to_file(altered_text, filename='altered_text.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(altered_text)

def main():
    text = read_text()
    language = detect_language(text)
    print(f"Detected language: {language}")

    analysis = stylometric_analysis(text)
    print(f"Word count: {analysis['word_count']}")
    print(f"Character count: {analysis['char_count']}")
    print(f"Average word length: {analysis['avg_word_length']:.2f}")
    print(f"Average sentence length (in words): {analysis['avg_sentence_length']:.2f}")
    print(f"Vocabulary richness (type-token ratio): {analysis['vocab_richness']:.2f}")

    save_analysis_to_file(analysis)
    print("Stylometric analysis saved to 'stylometric_analysis.txt'.")

    altered_text = replace_words(text)
    save_altered_text_to_file(altered_text)
    print("Altered text saved to 'altered_text.txt'.")

    # keywords = extract_keywords(text)
    # sentences = generate_sentences(keywords)
    # for sentence in sentences:
    #     print(sentence)

if __name__ == "__main__":
    main()
