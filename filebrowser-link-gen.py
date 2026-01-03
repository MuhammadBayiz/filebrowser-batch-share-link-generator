import requests
import csv
import os
import time

# =================================================================
# CONFIGURATION
# =================================================================
# 1. Your FileBrowser URL (e.g., https://browser.yourdomain.com)
BASE_URL = "https://YOUR_FILEBROWSER_URL"

# 2. The directory inside FileBrowser you want to scan (e.g., /Movies), Note the -r `PATH` is considered before the target_dir.
TARGET_DIR = "/YOUR_FOLDER_PATH"

# 3. YOUR JWT TOKEN (X-Auth Header)
# HOW TO GET THIS: 
# - Log in to your FileBrowser WebUI.
# - Open Browser DevTools (F12) -> Network Tab.
# - Click on any file/folder. 
# - Find a request to /api/resources/ and copy the 'X-Auth' value from Request Headers.
AUTH_TOKEN = "PASTE_YOUR_JWT_HERE"

# Extensions to filter (Add more if needed)
VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm')

# =================================================================
# HEADERS (Matching standard browser requests to avoid 403/400 errors)
# =================================================================
HEADERS = {
    "X-Auth": AUTH_TOKEN,
    "Content-Type": "text/plain;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BatchLinker/1.0",
    "Accept": "*/*"
}

def get_items_recursive(path):
    """Recursively fetches all file paths from the FileBrowser API."""
    video_files = []
    url = "{}/api/resources{}".format(BASE_URL, path)
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("Error {}: Skipping {}".format(response.status_code, path))
            return []
        
        data = response.json()
        if 'items' in data:
            for item in data['items']:
                # Skip hidden files/folders
                if item['name'].startswith('.'): continue
                
                if item['isDir']:
                    video_files.extend(get_items_recursive(item['path']))
                elif item['path'].lower().endswith(VIDEO_EXTENSIONS):
                    video_files.append(item['path'])
        return video_files
    except Exception as e:
        print("Request failed: {}".format(e))
        return []

def create_share(file_path):
    """Sends a POST request to generate a public share hash."""
    url = "{}/api/share{}".format(BASE_URL, file_path)
    # Sending empty raw data as per FileBrowser API requirements for default shares
    raw_data = "{}" 
    
    try:
        response = requests.post(url, headers=HEADERS, data=raw_data)
        if response.status_code == 200:
            return response.json().get('hash')
        return None
    except:
        return None

def save_csv(data, filename='file_links.csv'):
    """Writes the results to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["File_Path", "Direct_URL"])
        writer.writeheader()
        writer.writerows(data)

def main():
    print("--- FileBrowser Batch Share Generator ---")
    print("Scanning: {}".format(TARGET_DIR))
    
    videos = get_items_recursive(TARGET_DIR)
    total = len(videos)
    print("Found {} files. Starting share generation...".format(total))

    results = []
    for i, path in enumerate(videos, 1):
        # 0.1s sleep prevents SQLite 'Database is Locked' errors on high-volume requests
        time.sleep(0.1) 
        
        share_hash = create_share(path)
        if share_hash:
            direct_url = "{}/api/public/dl/{}".format(BASE_URL, share_hash)
            print("[{}/{}] Created: {}".format(i, total, os.path.basename(path)))
            results.append({"File_Path": path, "Direct_URL": direct_url})
        else:
            print("[{}/{}] FAILED: {}".format(i, total, path))

        # Save progress every 50 files
        if i % 50 == 0:
            save_csv(results)

    save_csv(results)
    print("\nProcess Complete! Output saved to file_links.csv")

if __name__ == "__main__":
    main()
