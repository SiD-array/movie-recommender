"""
Improved Movie Recommendation Model Builder

This script rebuilds the recommendation model with several improvements:
1. TF-IDF instead of Count Vectorizer (better word weighting)
2. Configurable n-gram range (capture phrases like "science fiction")
3. Optimized parameters based on movie domain

Usage:
    python build_improved_model.py
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def load_current_model():
    """Load the existing movie data."""
    print("[*] Loading current movie data...")
    movies_dict = pickle.load(open('models/movies_dict.pkl', 'rb'))
    df = pd.DataFrame(movies_dict)
    print(f"    Loaded {len(df)} movies")
    return df


def build_tfidf_model(df, max_features=5000, ngram_range=(1, 2)):
    """
    Build improved similarity matrix using TF-IDF.
    
    Why TF-IDF over Count Vectorizer?
    ---------------------------------
    1. Term Frequency (TF): How often a word appears in a document
    2. Inverse Document Frequency (IDF): Penalizes common words
    
    Example:
    - "action" appears in 1000 movies -> low IDF -> low weight
    - "jamescameron" appears in 10 movies -> high IDF -> high weight
    
    This means unique characteristics get more importance!
    
    Parameters:
    -----------
    max_features : int
        Maximum vocabulary size. Higher = more detailed but slower.
    ngram_range : tuple
        (1, 2) means unigrams AND bigrams.
        Captures "science fiction" as a single feature, not just "science" + "fiction"
    """
    print("\n[*] Building TF-IDF model...")
    print(f"    Max features: {max_features}")
    print(f"    N-gram range: {ngram_range}")
    
    # TF-IDF Vectorizer with optimized settings
    tfidf = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        stop_words='english',
        # Sublinear TF: use log(1 + tf) instead of tf
        # Why? Diminishing returns - 10 occurrences isn't 10x more important than 1
        sublinear_tf=True,
        # Minimum document frequency - ignore very rare words (typos, etc.)
        min_df=2,
        # Maximum document frequency - ignore words in >80% of movies
        max_df=0.8,
    )
    
    print("    Fitting TF-IDF vectorizer...")
    tfidf_matrix = tfidf.fit_transform(df['tags'])
    
    print(f"    Matrix shape: {tfidf_matrix.shape}")
    print(f"    Vocabulary size: {len(tfidf.vocabulary_)}")
    print(f"    Sparsity: {(1 - tfidf_matrix.nnz / (tfidf_matrix.shape[0] * tfidf_matrix.shape[1])) * 100:.1f}%")
    
    # Show top features by IDF (most discriminative)
    feature_names = tfidf.get_feature_names_out()
    idf_scores = tfidf.idf_
    top_idf_idx = np.argsort(idf_scores)[-10:]
    print("\n    Top 10 most discriminative features (highest IDF):")
    for idx in reversed(top_idf_idx):
        print(f"      - {feature_names[idx]}: {idf_scores[idx]:.2f}")
    
    return tfidf_matrix, tfidf


def compute_similarity(tfidf_matrix):
    """
    Compute cosine similarity matrix.
    
    Why Cosine Similarity?
    ----------------------
    - Measures angle between vectors, not magnitude
    - Two movies with same themes but different description lengths
      will still have high similarity
    - Range: [0, 1] - easy to interpret as percentage match
    """
    print("\n[*] Computing cosine similarity matrix...")
    similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
    print(f"    Shape: {similarity.shape}")
    print(f"    Value range: [{similarity.min():.4f}, {similarity.max():.4f}]")
    print(f"    Mean similarity: {similarity.mean():.4f}")
    return similarity


def compare_models(df, old_similarity, new_similarity, test_movies=None):
    """Compare old and new model recommendations."""
    if test_movies is None:
        test_movies = ['Avatar', 'The Dark Knight', 'Titanic', 'The Matrix', 'Toy Story']
    
    print("\n" + "=" * 70)
    print("MODEL COMPARISON")
    print("=" * 70)
    
    for movie_name in test_movies:
        matches = df[df['title'].str.lower() == movie_name.lower()]
        if len(matches) == 0:
            print(f"\n[!] Movie not found: {movie_name}")
            continue
            
        idx = matches.index[0]
        
        print(f"\n### {movie_name} ###")
        print("-" * 50)
        
        # Old model recommendations
        old_scores = list(enumerate(old_similarity[idx]))
        old_scores = sorted(old_scores, key=lambda x: x[1], reverse=True)[1:6]
        
        # New model recommendations
        new_scores = list(enumerate(new_similarity[idx]))
        new_scores = sorted(new_scores, key=lambda x: x[1], reverse=True)[1:6]
        
        print(f"{'Rank':<5} {'OLD MODEL':<35} {'NEW MODEL (TF-IDF)':<35}")
        print("-" * 75)
        
        for i, ((old_idx, old_score), (new_idx, new_score)) in enumerate(zip(old_scores, new_scores), 1):
            old_title = df.iloc[old_idx]['title'][:30]
            new_title = df.iloc[new_idx]['title'][:30]
            print(f"{i:<5} {old_title:<30} ({old_score:.1%})  {new_title:<30} ({new_score:.1%})")


def save_model(similarity, output_path='models/similarity_tfidf.pkl'):
    """Save the new similarity matrix."""
    print(f"\n[*] Saving improved model to {output_path}...")
    with open(output_path, 'wb') as f:
        pickle.dump(similarity, f)
    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"    Saved! File size: {file_size:.1f} MB")


def main():
    print("=" * 60)
    print("IMPROVED MODEL BUILDER")
    print("=" * 60)
    
    # Load data
    df = load_current_model()
    
    # Load old similarity for comparison
    print("\n[*] Loading original similarity matrix for comparison...")
    old_similarity = pickle.load(open('models/similarity.pkl', 'rb'))
    
    # Build new TF-IDF model
    tfidf_matrix, tfidf = build_tfidf_model(df)
    
    # Compute new similarity
    new_similarity = compute_similarity(tfidf_matrix)
    
    # Compare models
    compare_models(df, old_similarity, new_similarity)
    
    # Save new model
    save_model(new_similarity)
    
    # Also save as the main model (backup old one first)
    print("\n[*] Backing up original model...")
    import shutil
    if not os.path.exists('models/similarity_original.pkl'):
        shutil.copy('models/similarity.pkl', 'models/similarity_original.pkl')
        print("    Original model backed up to similarity_original.pkl")
    
    print("\n[*] Replacing main model with improved version...")
    shutil.copy('models/similarity_tfidf.pkl', 'models/similarity.pkl')
    print("    Done! The app will now use the improved model.")
    
    print("\n" + "=" * 60)
    print("IMPROVEMENT SUMMARY")
    print("=" * 60)
    print("""
    OLD MODEL (Count Vectorizer):
    - Equal weight for all words
    - "action" = "christophernolan" in importance
    - Simple word counts
    
    NEW MODEL (TF-IDF):
    - Rare words get higher weight (director names, unique keywords)
    - Common words get lower weight (action, love, movie)
    - Bigrams captured (e.g., "science fiction" as single feature)
    - Sublinear TF scaling (diminishing returns for repeated words)
    
    Result: More nuanced, discriminative recommendations!
    """)
    
    print("[OK] Restart the Streamlit app to see improved recommendations!")


if __name__ == "__main__":
    main()
