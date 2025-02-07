import os
import string
from collections import Counter
from sacremoses import MosesTokenizer
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# File paths
vocab_spreadsheet = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/vocab_files/combined_vocab_data.xlsx'
output_topics_file = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/vocab_files/improved_topics.xlsx'

# Parameters
n_topics = 10  # Number of topics to generate
threshold = 5   # Frequency threshold for rare words

# Initialize Moses tokenizer
tokenizer = MosesTokenizer()

def preprocess_text(word_freq_df):
    """
    Preprocess the text by removing stopwords, punctuations, and applying thresholds.
    Returns a filtered vocabulary as a single pseudo-document.
    """
    stop_words = set(ENGLISH_STOP_WORDS)
    punctuations = set(string.punctuation)

    # Ensure valid data and convert "Word" column to strings
    word_freq_df = word_freq_df.dropna(subset=["Word", "Frequency"]).copy()
    word_freq_df.loc[:, "Word"] = word_freq_df["Word"].astype(str)

    # Filter out stopwords, punctuations, and rare words below threshold
    filtered_words = [
        row["Word"].lower() for _, row in word_freq_df.iterrows()
        if row["Frequency"] >= threshold and row["Word"].lower() not in stop_words and row["Word"] not in punctuations
    ]

    # Combine filtered words into a single pseudo-document
    return ' '.join(filtered_words)

def prepare_document_term_matrix(filtered_text):
    """
    Create a document-term matrix using CountVectorizer.
    """
    vectorizer = CountVectorizer()
    document_term_matrix = vectorizer.fit_transform([filtered_text])  # Single pseudo-document
    feature_names = vectorizer.get_feature_names_out()
    return document_term_matrix, feature_names

def generate_topics(document_term_matrix, feature_names, n_topics=10, n_top_words=10):
    """
    Generate topics using LDA and return the top words per topic.
    """
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, max_iter=10)
    lda.fit(document_term_matrix)

    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topics.append({'Topic': f"Topic {topic_idx + 1}", 'Words': ', '.join(top_words)})

    return pd.DataFrame(topics)

def process_and_generate_topics(vocab_spreadsheet, output_topics_file, n_topics=10, threshold=5):
    """
    Load the vocabulary data, preprocess it, generate topics, and save the results.
    """
    # Load the combined vocabulary data
    vocab_df = pd.read_excel(vocab_spreadsheet)

    # Preprocess text
    filtered_text = preprocess_text(vocab_df)

    # Prepare document-term matrix
    document_term_matrix, feature_names = prepare_document_term_matrix(filtered_text)

    # Generate topics
    topics_df = generate_topics(document_term_matrix, feature_names, n_topics=n_topics)

    # Save topics to an Excel file
    topics_df.to_excel(output_topics_file, index=False)
    print(f"Improved topics saved to {output_topics_file}")

# Run the script
process_and_generate_topics(vocab_spreadsheet, output_topics_file, n_topics=n_topics, threshold=threshold)
