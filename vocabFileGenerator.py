import os
from collections import Counter
from sacremoses import MosesTokenizer
import pandas as pd 

# Directory paths for parsed text and paratext files
input_directory = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/Parsed_texts/'
output_directory = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/vocab_files/'
vocab_spreadsheet = os.path.join(output_directory, 'vocab_data.xlsx')  # Excel file to store vocab
threshold = 5

# Initialize Moses tokenizer
tokenizer = MosesTokenizer()

def tokenize_and_count_words(text):
    """Tokenize the text and return a Counter of word frequencies."""
    # Tokenize text using Moses tokenizer
    tokens = tokenizer.tokenize(text, return_str=False)
    # Use Counter to count word frequencies
    word_counts = Counter(tokens)
    return word_counts

def process_file(file_path, output_path, threshold):
    """Process a single text file to generate a vocabulary list."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Tokenize and count word frequencies
    word_counts = tokenize_and_count_words(text)

    # Apply frequency threshold to filter out less frequent words
    filtered_word_counts = {word: count for word, count in word_counts.items() if count >= threshold}

    # Save vocabulary to output file
    with open(output_path, 'w', encoding='utf-8') as f_out:
        for word, count in sorted(filtered_word_counts.items(), key=lambda x: -x[1]):
            f_out.write(f"{word}\t{count}\n")

def process_files(input_directory, output_directory, threshold):
    """Process all files in the input directory."""
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Process each file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('_parsed_text.txt') or filename.endswith('_footnotes.txt'):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, f"{filename}_vocab.txt")
            print(f"Processing {filename}...")

            # Process the file to create a vocabulary list
            process_file(input_file, output_file, threshold)
            print(f"Vocabulary list saved to {output_file}")

# Run the script
process_files(input_directory, output_directory, threshold)
