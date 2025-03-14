import os
import re
import requests
from urllib.parse import urlparse

def download_images_from_markdown(md_file, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Read Markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find Markdown image links ![alt text](url)
    img_pattern = re.compile(r'!\[.*?\]\((https?://.*?)\)')
    
    # Find all image URLs
    matches = img_pattern.findall(content)
    
    for img_url in matches:
        try:
            # Parse filename from URL
            parsed_url = urlparse(img_url)
            img_name = os.path.basename(parsed_url.path)
            local_path = os.path.join(output_folder, img_name)
            
            # Download image
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                with open(local_path, 'wb') as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                
                # Replace URL in content with local path
                content = content.replace(img_url, local_path)
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
    markdown_file = "content/posts/beers-of-myanmar/index.md"  # Change this to your Markdown file
    output_directory = "static/images/"  # Folder to save images
    download_images_from_markdown(markdown_file, output_directory)
