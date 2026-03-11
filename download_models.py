import urllib.request
import os

def download_models():
    """
    Downloads the pre-trained MobileNet SSD files.
    """
    model_dir = "models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    files = {
        "deploy.prototxt": "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt",
        "mobilenet_iter_73000.caffemodel": "https://github.com/chuanqi305/MobileNet-SSD/raw/master/mobilenet_iter_73000.caffemodel"
    }

    print("\n" + "="*50)
    print("      AI MODEL DOWNLOADER")
    print("="*50)
    
    for filename, url in files.items():
        filepath = os.path.join(model_dir, filename)
        if not os.path.exists(filepath):
            print(f"[*] Downloading {filename}...")
            print(f"    Source: {url}")
            try:
                urllib.request.urlretrieve(url, filepath)
                size = os.path.getsize(filepath)
                print(f"[+] Successfully downloaded {filename} ({size/1024/1024:.2f} MB)")
            except Exception as e:
                print(f"[!] Failed to download {filename}: {e}")
        else:
            size = os.path.getsize(filepath)
            print(f"[-] {filename} already exists ({size/1024/1024:.2f} MB).")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    download_models()
