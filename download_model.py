# download_models.py
import gdown
import os


def download_models():
    # Create directory if it doesn't exist
    os.makedirs('models', exist_ok=True)

    # Download files from Google Drive
    url = 'https://drive.google.com/file/d/1J1tLJ9-DXmAA7my9wpq6F-AKg-sKsZQ_/view?usp=drive_link'
    output = 'models/similarity.pkl'
    gdown.download(url, output, quiet=False)

    print("Models downloaded successfully!")


if __name__ == "__main__":
    download_models()