import os
from collections import Counter
from sacremoses import MosesTokenizer
import pandas as pd

# Directory paths for parsed text and paratext files
input_directory = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/Parsed_texts/'
output_directory = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/vocab_files/'
vocab_spreadsheet = os.path.join(output_directory, 'combined_vocab_data.xlsx')  # Excel file to store vocab

threshold = 5  # Set your threshold here, easily changeable

# Initialize Moses tokenizer
tokenizer = MosesTokenizer()

def tokenize_and_count_words(text):
    """Tokenize the text and return a Counter of word frequencies."""
    # Tokenize text using Moses tokenizer
    tokens = tokenizer.tokenize(text, return_str=False)
    # Use Counter to count word frequencies
    word_counts = Counter(tokens)
    return word_counts

def process_file(file_path):
    """Process a single text file to generate word counts."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Tokenize and count word frequencies
    word_counts = tokenize_and_count_words(text)
    return word_counts

def process_files(input_directory, threshold):
    """Process all files in the input directory and create a combined vocabulary list."""
    combined_word_counts = Counter()

    # Process each file in the input directory
    for filename in os.listdir(input_directory):
        # Ensure we're only processing relevant text files
        if (filename.endswith('_parsed_text.txt') or filename.endswith('_footnotes.txt')) and not filename.startswith('.'):
            input_file = os.path.join(input_directory, filename)
            print(f"Processing {filename}...")

            # Update the combined word counts with counts from the current file
            file_word_counts = process_file(input_file)
            combined_word_counts.update(file_word_counts)

    # Apply frequency threshold to filter out less frequent words
    filtered_word_counts = {word: count for word, count in combined_word_counts.items() if count >= threshold}

    # Convert the filtered word counts to a DataFrame
    vocab_df = pd.DataFrame(list(filtered_word_counts.items()), columns=['Word', 'Frequency'])

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Save the combined vocabulary to an Excel file
    vocab_df.to_excel(vocab_spreadsheet, index=False)
    print(f"Combined vocabulary spreadsheet saved to: {vocab_spreadsheet}")

# Run the script
process_files(input_directory, threshold)
