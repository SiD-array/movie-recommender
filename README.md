# Movie Recommender System 🎬

A content-based movie recommendation system that suggests similar movies based on the user's selection. The system analyzes movie features such as genres, cast, crew, and plot keywords to make personalized recommendations.

## Setup
1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run `python download_models.py` to download the required model files
4. Run the application: `streamlit run app.py`

## Features

- **Content-Based Filtering**: Uses movie metadata to find similar movies
- **Interactive UI**: Clean and user-friendly interface built with Streamlit
- **Real-time Recommendations**: Get instant movie suggestions with movie posters
- **TMDB Integration**: Fetches movie posters and additional information from The Movie Database (TMDB)

## Tech Stack

- **Backend**: Python, scikit-learn
- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **API Integration**: TMDB API
- **Data Source**: TMDB 5000 Movie Dataset

## Project Structure

```
movie_recommender/
│
├── data/
│   ├── movies_dict.pkl        # Processed movie data
│   └── similarity.pkl         # Similarity matrix
│
├── notebooks/
│   └── model_development.ipynb    # Data processing and model development
│
├── app.py                     # Streamlit frontend application
├── requirements.txt           # Project dependencies
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd movie-recommender
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Get TMDB API Key:
- Visit [TMDB website](https://www.themoviedb.org/)
- Create an account and request an API key
- Replace `your_tmdb_api_key_here` in `app.py` with your actual API key

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Select a movie from the dropdown menu

4. Click "Get Recommendations" to see similar movies

## How It Works

### Data Processing
1. Extracts relevant features from TMDB dataset including:
   - Genres
   - Keywords
   - Cast
   - Crew
   - Overview

2. Creates tags by combining these features

3. Applies text preprocessing:
   - Removes stopwords
   - Applies stemming
   - Handles whitespace issues

### Model
1. Uses Count Vectorization (Bag of Words) to convert text data into numerical vectors
2. Creates a similarity matrix using cosine similarity
3. Recommends movies based on similarity scores

## API Integration

The system integrates with TMDB API to fetch:
- Movie posters
- Additional movie information
- Real-time data updates

## Performance Considerations

- The model uses the top 5000 most frequent words for vectorization
- Similarity calculations are optimized using scikit-learn's implementations
- Movie posters are cached to improve loading times

## Future Improvements

Potential enhancements for the project:
1. Add collaborative filtering
2. Implement user authentication
3. Add movie ratings and reviews
4. Include movie trailers
5. Add advanced filtering options
6. Implement a rating prediction system

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- TMDB for providing the movie dataset and API
- Streamlit for the awesome framework
- scikit-learn for machine learning tools

## Contact

For any queries or suggestions, please reach out to [Your Name/Email]
