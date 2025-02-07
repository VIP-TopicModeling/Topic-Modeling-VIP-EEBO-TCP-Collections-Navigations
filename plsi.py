import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# File paths
vocab_spreadsheet = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/vocab_files/combined_vocab_data.xlsx'
output_topics_file = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/vocab_files/topics.xlsx'

# Parameters
n_topics = 10  # Number of topics to generate
threshold = 5   # Frequency threshold (used during pre-processing)

# Load the combined vocabulary data
vocab_df = pd.read_excel(vocab_spreadsheet)

# Step 1: Prepare the Document-Term Matrix
def prepare_document_term_matrix(vocab_df):
    # Create a pseudo-document combining all terms weighted by frequency
    pseudo_document = ' '.join([f"{row['Word']} " * row['Frequency'] for _, row in vocab_df.iterrows()])

    # Use CountVectorizer to tokenize and create a document-term matrix
    vectorizer = CountVectorizer()
    document_term_matrix = vectorizer.fit_transform([pseudo_document])  # Single pseudo-document
    feature_names = vectorizer.get_feature_names_out()

    return document_term_matrix, feature_names

# Prepare the document-term matrix
document_term_matrix, feature_names = prepare_document_term_matrix(vocab_df)

# Step 2: Apply pLSI (via Latent Dirichlet Allocation in sklearn)
lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, max_iter=10)
lda.fit(document_term_matrix)

# Step 3: Extract and Save Topics
def save_topics(lda_model, feature_names, output_file, n_top_words=10):
    topics = []
    for topic_idx, topic in enumerate(lda_model.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topics.append({'Topic': f"Topic {topic_idx + 1}", 'Words': ', '.join(top_words)})

    # Convert to DataFrame and save to Excel
    topics_df = pd.DataFrame(topics)
    topics_df.to_excel(output_file, index=False)
    print(f"Topics saved to {output_file}")

# Save the topics to an Excel file
save_topics(lda, feature_names, output_topics_file)
