# FileBrowser Batch Link Generator

**Automate public direct URL generation for large media libraries on FileBrowser.**

### 📖 Description

When managing large media servers (like Kurdish Cinema or streaming platforms), generating public share links for thousands of files manually via the FileBrowser WebUI is impossible.

This Python script recursively scans a specific directory on your FileBrowser instance, creates a permanent public share for every video file found, and exports the results into a clean **CSV file**. This CSV can then be easily imported into a SQL database (MySQL, PostgreSQL, etc.) or a spreadsheet.

### ✨ Features

* **Recursive Scanning:** Finds files in all subfolders.
* **Smart Filtering:** Only processes video formats (`.mp4`, `.mkv`, etc.) and ignores hidden system files/folders (like `.Recycle_bin`).
* **Rate Limiting:** Includes a small delay to prevent SQLite "Database is Locked" errors during high-volume requests.
* **Direct URLs:** Generates the raw `/api/public/dl/` links ready for streaming or downloading.

---

### 🚀 How to Use

#### 1. Prerequisites

Ensure you have Python 3 installed and the `requests` library:

```bash
pip install requests

```

#### 2. Obtain your JWT (X-Auth Token)

The script requires authentication to talk to the FileBrowser API.

1. Log in to your **FileBrowser WebUI** via Chrome or Firefox.
2. Press `F12` to open **Developer Tools** and go to the **Network** tab.
3. Refresh the page or click on any folder.
4. Find a request named `resources` or `items`.
5. Look at the **Request Headers** and copy the value of `X-Auth`. This is your JWT.

#### 3. Configure the Script

Open `filebrowsergenerator.py` and update the following variables:

* `BASE_URL`: Your FileBrowser URL (e.g., `https://browser.yourdomain.com`).
* `TARGET_DIR`: The folder path inside FileBrowser you want to scan.
* `AUTH_TOKEN`: The `X-Auth` token you copied in the previous step.

#### 4. Run the Script

```bash
python3 filebrowsergenerator.py

```

---

### 📊 Output

The script will generate a file named `file_links.csv` in the same directory.

| File_Path | Direct_URL |
| --- | --- |
| /Movies/Action/Film.mp4 | [https://yourdomain.com/api/public/dl/Td7rM144](https://www.google.com/search?q=https://yourdomain.com/api/public/dl/Td7rM144) |
| /Movies/Drama/Show.mkv | [https://yourdomain.com/api/public/dl/Ab12C345](https://www.google.com/search?q=https://yourdomain.com/api/public/dl/Ab12C345) |

---

### ⚠️ Important Notes

* **Database Safety:** The `time.sleep(0.1)` is crucial. If you have a very powerful server with SSD storage, you can lower this, but for most SQLite setups, keeping it avoids `Error 500` or `Error 400`.
* **Token Expiry:** JWT tokens usually expire. If the script starts returning `401 Unauthorized`, simply grab a fresh `X-Auth` token from your browser.

---

### 🤝 Contributing

Feel free to fork this repository, report issues, or submit pull requests to improve the script!
