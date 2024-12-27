import requests
import os

def download_file(url, save_path):
    """
    Download a file from the given URL if it doesn't already exist locally.
    """
    if not os.path.exists(save_path):
        print(f"Downloading {save_path}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File saved to {save_path}")
    else:
        print(f"{save_path} already exists locally.")

# File URLs
file_urls = {
    "similarity.pkl": "https://drive.google.com/file/d/1J1tLJ9-DXmAA7my9wpq6F-AKg-sKsZQ_/view?usp=sharing",
    "movies_dict.pkl": "https://drive.google.com/file/d/1iLa6zxc06PjB5iJuJV_KCvi48akA8IWe/view?usp=sharing",
}

# Ensure the models directory exists
os.makedirs("models", exist_ok=True)

# Download files
for file_name, file_url in file_urls.items():
    download_file(file_url, f"models/{file_name}")
