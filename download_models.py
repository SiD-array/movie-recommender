import gdown
import os

def download_models():
    os.makedirs('models', exist_ok=True)
    
    # Update these IDs from your Google Drive share links
    files = {
        'similarity.pkl': '1J1tLJ9-DXmAA7my9wpq6F-AKg-sKsZQ_',
        'movies_dict.pkl': '1iLa6zxc06PjB5iJuJV_KCvi48akA8IWe'
    }
    
    for filename, file_id in files.items():
        print(f"Downloading {filename}...")
        url = f'https://drive.google.com/uc?id={file_id}'
        output = f'models/{filename}'
        gdown.download(url, output, quiet=False)
        print(f"Successfully downloaded {filename}")

if __name__ == "__main__":
    download_models()
