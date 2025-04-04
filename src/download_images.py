import os
import re
import requests
from urllib.parse import urlparse
import time
import re
import urllib.parse


def modify_blogger_url(url: str) -> str:
    # Ensure the URL is from Blogger before making modifications
    if "blogger.googleusercontent.com" not in url:
        return url
    
    # Pattern to match size indicators (e.g., "s288" or "s<value>") and replace with "s0"
    url = re.sub(r'/s\d+/', '/s0/', url)
    
    # Pattern to match "w<width>-h<height>" and replace it with "s0"
    url = re.sub(r'/w\d+-h\d+/', '/s0/', url)
    
    return url


def download_images_from_markdown(md_file, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Read Markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find Markdown image links ![alt text](url)
    # pattern = r'\((https?://blogger\.googleusercontent\.com[^)]+/([^/]+\.(?:jpeg|jpg|png|gif|webp)))\)'
    img_pattern = re.compile(r'!\[.*?\]\((https?://.*?)\)')
    # img_pattern = re.compile(pattern)

    # Find all image URLs
    matches = img_pattern.findall(content)
    
    for img_url in matches:
        try:
            # Get the original image
            orig_img_url = modify_blogger_url(img_url)

            # Parse filename from URL
            parsed_url = urlparse(img_url)
            img_name = os.path.basename(parsed_url.path)
            slug_img_name = urllib.parse.unquote(img_name).replace(" ","")
            local_path = os.path.join(output_folder, slug_img_name)
            time.sleep(1) # I don't know if this is needed, but trying to prevent being rate limited.
            # Download image
            response = requests.get(modify_blogger_url(img_url), stream=True)
            if response.status_code == 200:
                with open(local_path, 'wb') as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                
                # Replace URL in content with local path
                content = content.replace(img_url, slug_img_name)

                print(f"Downloaded: {img_url} -> {local_path}")
            else:
                print(f"Failed to download: {img_url}")
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")
    
    # Write updated Markdown content
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Markdown file updated successfully!")

# Example usage
if __name__ == "__main__":
    start_directory = "content/posts"
    for filename in os.scandir(start_directory):
        if filename.is_dir():
            print(filename.path)

            
            markdown_file = filename.path + "/index.md"
            download_images_from_markdown(markdown_file, filename.path)
 
