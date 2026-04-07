import shutil
import glob
import os

import browser_cookie3

def copy_firefox_cookies(username: str, destination_folder: str):
    source_pattern = f"/mnt/c/Users/{username}/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite"

    # Find matching files (expands the *)
    matching_files = glob.glob(source_pattern)

    if matching_files:
        source_path = matching_files[0]

        destination_path = os.path.join(
            destination_folder, "copied_cookies.sqlite"
        )

        try:
            shutil.copy2(
                source_path, destination_path
            )  # copy2 preserves metadata like permissions and timestamps
            print(f"File copied successfully: {source_path} -> {destination_path}")
        except Exception as e:
            print(f"Error copying file: {e}")
    else:
        print(
            "No matching cookies.sqlite file found. Ensure Firefox is installed and has profiles."
        )
        
def load_cookies_from_file(cookie_file_path: str, domain_name: str = "") -> list[dict]:
    cookies = browser_cookie3.firefox(
        cookie_file=cookie_file_path,
        domain_name=domain_name,
    )

    # Convert browser_cookie3 Cookie objects to dict format
    cookies_dict = [
        {
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path,
            "httpOnly": True if c._rest else False,
            "secure": bool(c.secure),
            "expires": int(c.expires) // 1000 if c.expires else None,
        }
        for c in cookies
    ]
    
    return cookies_dict
