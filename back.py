import os
import cloudscraper
import re
import libtorrent as lt
import time
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}


def download_file(link, folder_path, progress_callback=None):
    if not link:

        print("Error: Please provide a link")
        return


    link = link.strip()

    if link.startswith("magnet:?"):
        return _download_magnet(link, folder_path, progress_callback)
    elif link.startswith("http://") or link.startswith("https://"):
        return _download_direct(link, folder_path, progress_callback)
    else:
        return False, "Error: Invalid link. Must start with http, https, or magnet:?"



def _download_direct(url, folder_path, progress_callback):
    match = re.search(r'/([^/]+\.(jpg|jpeg|png|gif|txt|mp4|zip|rar|exe))$', url, re.IGNORECASE)
    filename = match.group(1) if match else "downloaded_file"
    final_save_path = os.path.join(folder_path, filename)

    scraper = cloudscraper.create_scraper()
    
    try:
        if progress_callback:
            progress_callback("Connecting to server...")
            
        r = scraper.get(url, headers=HEADERS)
        if r.status_code == 200:
            with open(final_save_path, "wb") as file:
                file.write(r.content)
            return True, f"Success! File saved to:\n{final_save_path}"
        else:
            return False, f"Failed HTTP. Status code: {r.status_code}"
    except Exception as e:
        return False, f"HTTP Network error: {e}"


def _download_magnet(magnet_link, folder_path, progress_callback):
    try:
        # 1. Start the BitTorrent Session
        ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
        
        # 2. Add the Magnet Link
        params = lt.parse_magnet_uri(magnet_link)
        params.save_path = folder_path
        handle = ses.add_torrent(params)

        # 3. Download Metadata (Finding Peers)
        if progress_callback:
            progress_callback("Finding peers and downloading metadata...")
            
        while not handle.has_metadata():
            time.sleep(1)

        # 4. Monitor the actual download
        torrent_name = handle.status().name
        
        while handle.status().state != lt.torrent_status.seeding:
            s = handle.status()
            
            # Send live updates back to the GUI
            if progress_callback:
                progress_msg = f"Downloading '{torrent_name}' | Progress: {s.progress * 100:.2f}% | Peers: {s.num_peers}"
                progress_callback(progress_msg)
                
            time.sleep(1)

        return True, f"Success! Torrent completely downloaded to:\n{folder_path}"
        
    except Exception as e:
        return False, f"libtorrent error: {e}"