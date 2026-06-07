import os, cloudscraper, re
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}



def download_file(url, folder_path):
        if not url:
            print("Error: Please provide both a link")
            return

        match = re.search(r'/([^/]+\.(jpg|png|txt))$', url, re.IGNORECASE)
        filename = match.group(1) if match else "downloaded_file.png"

        final_save_path = os.path.join(folder_path, filename)

        scraper = cloudscraper.create_scraper()
        print("Downloading...")

        try:
            r = scraper.get(url, headers=headers)

            if r.status_code == 200:
                with open(final_save_path, "wb") as file:
                    file.write(r.content)
                print(f"File downloaded successfully to:\n{final_save_path}")
            else:
                print(f"Failed to download. Status code: {r.status_code}")
        except Exception as e:
            print(f"A network error occurred: {e}")
