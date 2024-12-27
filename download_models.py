import requests
import os

def download_file(url, save_path):
    if not os.path.exists(save_path):
        print(f"Downloading {save_path}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {save_path}")

# Provide the URL for your file
url = "https://your-cloud-link/similarity.pkl"
save_path = "models/similarity.pkl"

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Download the file
download_file(url, save_path)
