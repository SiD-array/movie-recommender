import gdown
import os

def download_models():
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)

    # File IDs from Google Drive links
    files = {
        'similarity.pkl': '1J1tLJ9-DXmAA7my9wpq6F-AKg-sKsZQ_',  # Replace with your file ID
        'movies_dict.pkl': '1iLa6zxc06PjB5iJuJV_KCvi48akA8IWe'  # Replace with your file ID
    }

    for filename, file_id in files.items():
        print(f"Downloading {filename}...")
        url = f'https://drive.google.com/uc?id={file_id}'
        output = f'models/{filename}'
        gdown.download(url, output, quiet=False)


if __name__ == "__main__":
    download_models()