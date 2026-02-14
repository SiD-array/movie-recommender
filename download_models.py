"""
Model Download Script for CineMatch Movie Recommender

This script downloads the pre-trained model files from Google Drive.
Run this before starting the Streamlit app for the first time.

Usage:
    python download_models.py
"""

import os
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def check_gdown():
    """Check if gdown is installed."""
    try:
        import gdown
        return True
    except ImportError:
        return False

def install_gdown():
    """Install gdown package."""
    print("[*] Installing gdown package...")
    os.system(f"{sys.executable} -m pip install gdown")

def download_models():
    """Download model files from Google Drive."""
    import gdown
    
    # Create models directory
    models_dir = 'models'
    os.makedirs(models_dir, exist_ok=True)
    
    # Model files with their Google Drive IDs
    files = {
        'similarity.pkl': '1J1tLJ9-DXmAA7my9wpq6F-AKg-sKsZQ_',
        'movies_dict.pkl': '1iLa6zxc06PjB5iJuJV_KCvi48akA8IWe'
    }
    
    print("=" * 50)
    print("CineMatch Model Downloader")
    print("=" * 50)
    print()
    
    success_count = 0
    
    for filename, file_id in files.items():
        output_path = os.path.join(models_dir, filename)
        
        # Check if file already exists
        if os.path.exists(output_path):
            print(f"[OK] {filename} already exists, skipping...")
            success_count += 1
            continue
        
        print(f"[..] Downloading {filename}...")
        url = f'https://drive.google.com/uc?id={file_id}'
        
        try:
            gdown.download(url, output_path, quiet=False)
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"[OK] Successfully downloaded {filename} ({file_size:.1f} MB)")
                success_count += 1
            else:
                print(f"[FAIL] Failed to download {filename}")
        except Exception as e:
            print(f"[FAIL] Error downloading {filename}: {str(e)}")
    
    print()
    print("=" * 50)
    
    if success_count == len(files):
        print("[OK] All model files downloaded successfully!")
        print()
        print("You can now run the app with:")
        print("   streamlit run app.py")
    else:
        print(f"[WARN] Downloaded {success_count}/{len(files)} files")
        print("   Some files may need to be downloaded manually.")
    
    print("=" * 50)

def verify_models():
    """Verify that model files exist and can be loaded."""
    import pickle
    
    models_dir = 'models'
    required_files = ['similarity.pkl', 'movies_dict.pkl']
    
    print()
    print("[*] Verifying model files...")
    
    all_valid = True
    for filename in required_files:
        filepath = os.path.join(models_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"[FAIL] Missing: {filename}")
            all_valid = False
            continue
        
        try:
            with open(filepath, 'rb') as f:
                pickle.load(f)
            print(f"[OK] Valid: {filename}")
        except Exception as e:
            print(f"[FAIL] Corrupted: {filename} - {str(e)}")
            all_valid = False
    
    return all_valid

def main():
    """Main entry point."""
    # Check and install gdown if needed
    if not check_gdown():
        install_gdown()
        
        # Re-check after installation
        if not check_gdown():
            print("[FAIL] Failed to install gdown. Please install manually:")
            print("   pip install gdown")
            sys.exit(1)
    
    # Download models
    download_models()
    
    # Verify models
    if verify_models():
        print()
        print("[OK] Setup complete! Ready to run the app.")
    else:
        print()
        print("[WARN] Some model files are missing or corrupted.")
        print("   Please try running this script again or download manually.")
        sys.exit(1)

if __name__ == "__main__":
    main()
