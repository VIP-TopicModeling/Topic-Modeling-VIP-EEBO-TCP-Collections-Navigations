import os
import string
from collections import Counter
from sacremoses import MosesTokenizer
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# File paths
vocab_spreadsheet = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/vocab_files/combined_vocab_data.xlsx'
output_topics_file = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/vocab_files/distinct_topics.xlsx'

# Parameters
n_topics = 5  # Number of topics to generate
threshold = 2   # Frequency threshold for rare words

# Initialize Moses tokenizer
tokenizer = MosesTokenizer()

def preprocess_text(word_freq_df):
    stop_words = set(ENGLISH_STOP_WORDS)
    punctuations = set(string.punctuation)

    word_freq_df = word_freq_df.dropna(subset=["Word", "Frequency"]).copy()
    word_freq_df.loc[:, "Word"] = word_freq_df["Word"].astype(str)

    filtered_words = [
        row["Word"].lower() for _, row in word_freq_df.iterrows()
        if row["Frequency"] >= threshold and row["Word"].lower() not in stop_words and row["Word"] not in punctuations
    ]
    return ' '.join(filtered_words)

def prepare_document_term_matrix(filtered_text):
    """
    Create a document-term matrix using CountVectorizer.
    """
    vectorizer = CountVectorizer()  # Remove max_df and min_df for a single pseudo-document
    document_term_matrix = vectorizer.fit_transform([filtered_text])
    feature_names = vectorizer.get_feature_names_out()
    return document_term_matrix, feature_names, vectorizer

def generate_topics(document_term_matrix, feature_names, n_topics=5, n_top_words=10):
    """
    Generate topics using LDA and return the top words per topic.
    """
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, max_iter=50, learning_decay=0.7)
    lda.fit(document_term_matrix)

    # Extract topics
    topics = []
    topic_distributions = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topics.append({'Topic': f"Topic {topic_idx + 1}", 'Words': ', '.join(top_words)})
        topic_distributions.append(topic)

    return pd.DataFrame(topics), np.array(topic_distributions)

def filter_duplicate_topics(topics_df, topic_distributions, similarity_threshold=0.9):
    unique_topics = []
    seen_indices = set()

    for i in range(len(topic_distributions)):
        if i in seen_indices:
            continue
        unique_topics.append(topics_df.iloc[i])
        for j in range(i + 1, len(topic_distributions)):
            similarity = cosine_similarity(
                topic_distributions[i].reshape(1, -1),
                topic_distributions[j].reshape(1, -1),
            )[0][0]
            if similarity > similarity_threshold:
                seen_indices.add(j)

    return pd.DataFrame(unique_topics)

def process_and_generate_topics(vocab_spreadsheet, output_topics_file, n_topics=5, threshold=5):
    vocab_df = pd.read_excel(vocab_spreadsheet)
    filtered_text = preprocess_text(vocab_df)
    document_term_matrix, feature_names, vectorizer = prepare_document_term_matrix(filtered_text)

    topics_df, topic_distributions = generate_topics(document_term_matrix, feature_names, n_topics=n_topics)
    distinct_topics_df = filter_duplicate_topics(topics_df, topic_distributions)

    distinct_topics_df.to_excel(output_topics_file, index=False)
    print(f"Distinct topics saved to {output_topics_file}")

# Run the script
process_and_generate_topics(vocab_spreadsheet, output_topics_file, n_topics=n_topics, threshold=threshold)
