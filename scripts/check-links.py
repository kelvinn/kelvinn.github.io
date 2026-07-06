#!/usr/bin/env python3
"""
Robust internal link checker for Hugo static sites.
More resilient than the original CI script to handle edge cases.
"""

import re
import sys
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def normalize_path(path):
    """Normalize file path for comparison."""
    return Path(path).resolve()

def check_internal_links(root_dir, public_dir):
    """Check for broken internal links in HTML files."""
    root_path = Path(root_dir).resolve()
    public_path = Path(public_dir).resolve()
    
    broken_links = []
    total_checked = 0
    files_with_issues = 0
    
    # Find all HTML files
    html_files = list(public_path.rglob("*.html"))
    logger.info(f"Found {len(html_files)} HTML files to check...")
    
    for html_file in sorted(html_files):
        total_checked += 1
        file_issues = []
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Could not read {html_file.relative_to(public_path)}: {e}")
            continue
        
        # Extract all href attributes
        links = re.findall(r'href=[\'"]([^\'"]*)[\'"]', content)
        
        for link in links:
            # Skip external links, mailto, tel, javascript, and anchors
            if (link.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', '#', 'data:')) or
                link.startswith('//')):
                continue
            
            # Handle relative and absolute links
            if link.startswith('/'):
                # Absolute path - remove leading slash and check in public
                link_path = public_path / link.lstrip('/')
            else:
                # Relative path - resolve relative to current HTML file
                link_path = html_file.parent / link
            
            # Check if file exists (with or without .html extension)
            if not link_path.exists():
                # Try with .html extension for relative paths
                if not link_path.suffix:
                    html_link_path = link_path.with_suffix('.html')
                    if html_link_path.exists():
                        continue  # Found with .html extension
                
                # Check for case sensitivity issues on Linux
                found_case_match = False
                if link_path.exists():
                    found_case_match = True
                else:
                    # Try case-insensitive match
                    parent_dir = link_path.parent
                    if parent_dir.exists():
                        for sibling in parent_dir.iterdir():
                            if sibling.name.lower() == link_path.name.lower() and sibling != link_path:
                                found_case_match = True
                                break
                
                if not found_case_match:
                    file_issues.append({
                        'link': link,
                        'file': str(link_path.relative_to(public_path))
                    })
            
            # Check if the resolved path is within public directory
            try:
                link_path.relative_to(public_path)
            except ValueError:
                # Link points outside public directory
                file_issues.append({
                    'link': link,
                    'file': f"EXTERNAL: {link_path}"
                })
        
        if file_issues:
            files_with_issues += 1
            broken_links.extend(file_issues)
            logger.warning(f"{html_file.relative_to(public_path)}:")
            for issue in file_issues:
                logger.warning(f"  - Broken link: {issue['link']} -> {issue['file']}")
    
    # Summary
    logger.info(f"\nLink Check Summary:")
    logger.info(f"  Files checked: {total_checked}")
    logger.info(f"  Files with broken links: {files_with_issues}")
    logger.info(f"  Total broken links: {len(broken_links)}")
    
    if broken_links:
        logger.error(f"\nFound {len(broken_links)} broken internal links!")
        if len(broken_links) > 20:
            logger.error(f"(Showing first 20 of {len(broken_links)})")
        for i, issue in enumerate(broken_links[:20], 1):
            logger.error(f"  {i}. {issue['link']} -> {issue['file']}")
        if len(broken_links) > 20:
            logger.error(f"  ... and {len(broken_links) - 20} more")
        return False
    else:
        logger.info("✅ All internal links are valid!")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check internal links in Hugo static site")
    parser.add_argument('--root', default='.', help='Root directory of the project')
    parser.add_argument('--public', default='public', help='Public directory with built HTML files')
    
    args = parser.parse_args()
    
    success = check_internal_links(args.root, args.public)
    sys.exit(0 if success else 1)