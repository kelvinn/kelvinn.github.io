import os
import re

def replace_google_image_urls(markdown_text):
    """Replace Picasa Web and Blogger Googleusercontent image URLs in markdown links with the image filename."""
    pattern = r'(\[!\[\]\((.*?)\)\]\()(https?://(?:picasaweb\.google\.com|blogger\.googleusercontent\.com)/.*?\))'
    return re.sub(pattern, r'\1\2)', markdown_text)

def process_markdown_files(directory):
    """Recursively process all 'index.md' files in subdirectories."""
    for root, dirs, files in os.walk(directory):
        if "index.md" in files:
            file_path = os.path.join(root, "index.md")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            updated_content = replace_google_image_urls(content)
            
            if content != updated_content:  # Only overwrite if changes were made
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print(f"Updated: {file_path}")
            else:
                print(f"No changes: {file_path}")

# Example usage
directory_path = "content/posts"  # Change this to your actual directory path
process_markdown_files(directory_path)
