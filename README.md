# CineMatch - Movie Recommender System

A content-based movie recommendation system that suggests similar movies based on your selection. Built with Python and Streamlit, featuring a modern Netflix-inspired UI and an optimized TF-IDF algorithm.

### [🎬 Try the Live Demo →](https://cinematch-movie-recommend.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit&logoColor=white)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.3+-orange?logo=scikit-learn&logoColor=white)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cinematch-movie-recommend.streamlit.app/)

## Features

- **Content-Based Filtering** - Analyzes movie metadata (genres, cast, crew, keywords, plot)
- **TF-IDF Algorithm** - Optimized vectorization with bigram support for better recommendations
- **Modern UI** - Netflix-inspired dark theme with smooth animations
- **Fast Performance** - Cached model loading and API responses
- **Secure** - API keys stored in secrets, not in code

## Demo

🔗 **Live App:** [cinematch-movie-recommend.streamlit.app](https://cinematch-movie-recommend.streamlit.app/)

Select any movie from the database of 4,800+ films and get instant recommendations!

## Run Locally

### Prerequisites

- Python 3.9+
- TMDB API Key ([Get one free](https://www.themoviedb.org/settings/api))

### Installation

```bash
# Clone the repository
git clone https://github.com/SiD-array/movie-recommender.git
cd movie-recommender

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure API key
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
# Edit secrets.toml and add your TMDB API key

# Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Project Structure

```
movie-recommender/
├── .streamlit/
│   ├── config.toml           # Streamlit theme & server config
│   └── secrets.toml.example  # API key template
├── models/
│   ├── movies_dict.pkl       # Processed movie data (4806 movies)
│   └── similarity.pkl        # TF-IDF similarity matrix (Git LFS)
├── app.py                    # Main Streamlit application
├── build_improved_model.py   # Script to rebuild/improve the model
├── download_models.py        # Script to download model files
├── requirements.txt          # Python dependencies
└── README.md
```

## Algorithm

### How It Works

The system uses **Content-Based Filtering** with **TF-IDF Vectorization**:

```
Movie Features → Text Preprocessing → TF-IDF Vectorization → Cosine Similarity → Recommendations
```

### TF-IDF (Term Frequency-Inverse Document Frequency)

Unlike simple word counting, TF-IDF weighs words by their importance:

| Word Type | Example | Weight |
|-----------|---------|--------|
| Rare (discriminative) | "christophernolan", "pixar" | **High** |
| Common (generic) | "action", "movie", "story" | **Low** |

**Formula:**
```
weight = log(1 + term_frequency) × log(total_documents / documents_containing_term)
```

### Features Used

- **Genres** - Action, Comedy, Drama, etc.
- **Keywords** - Plot-specific tags
- **Cast** - Top actors
- **Crew** - Director
- **Overview** - Plot summary

### Key Optimizations

| Feature | Benefit |
|---------|---------|
| **Bigrams** | Captures phrases like "science fiction" as single features |
| **Sublinear TF** | Diminishing returns for repeated words |
| **Document Frequency Limits** | Filters out typos and overly common words |

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| ML/NLP | scikit-learn (TF-IDF, Cosine Similarity) |
| Data | Pandas, NumPy |
| API | TMDB API |
| Dataset | TMDB 5000 Movie Dataset |

## Rebuilding the Model

To rebuild or customize the recommendation model:

```bash
python build_improved_model.py
```

This script allows you to adjust:
- `max_features` - Vocabulary size
- `ngram_range` - Unigrams, bigrams, etc.
- `min_df` / `max_df` - Document frequency thresholds

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [TMDB](https://www.themoviedb.org/) for the movie database and API
- [Streamlit](https://streamlit.io/) for the web framework
- [scikit-learn](https://scikit-learn.org/) for ML tools

## Contact

**Siddharth Bhople** - sid.work0403@gmail.com

Project: [github.com/SiD-array/movie-recommender](https://github.com/SiD-array/movie-recommender)
