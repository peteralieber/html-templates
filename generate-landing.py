#!/usr/bin/env python3

"""
Script to generate the main landing page (index.html) by scanning
subdirectories for template.json files.
"""

import json
import os
import re
import sys
from pathlib import Path
from html import escape as html_escape


def escape_html(text):
    """Escape HTML special characters to prevent XSS"""
    return html_escape(text, quote=True)


def is_valid_path(template_path):
    """
    Validate that the path is a safe relative path within the repository
    """
    # Must be a relative path (not starting with / or containing ..)
    if template_path.startswith('/') or '..' in template_path:
        return False
    
    # Should not be an external URL
    if re.match(r'^[a-z]+://', template_path, re.IGNORECASE):
        return False
    
    return True


def find_templates():
    """Get all subdirectories that contain a template.json file"""
    templates = []
    root_dir = Path(__file__).parent
    
    # Read all items in the root directory
    try:
        items = [item for item in root_dir.iterdir() if item.is_dir()]
    except Exception as e:
        print(f"Error reading directory: {e}", file=sys.stderr)
        return templates
    
    # Filter for directories only (exclude hidden directories)
    directories = [item for item in items if not item.name.startswith('.')]
    
    # Check each directory for template.json
    for directory in directories:
        template_json_path = directory / 'template.json'
        
        if template_json_path.exists():
            try:
                with open(template_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Validate required fields
                if not data.get('title') or not data.get('description') or not data.get('path'):
                    print(f"Warning: Skipping {template_json_path}: missing required fields", file=sys.stderr)
                    continue
                
                # Validate path safety
                if not is_valid_path(data['path']):
                    print(f"Warning: Skipping {template_json_path}: invalid path \"{data['path']}\"", file=sys.stderr)
                    continue
                
                templates.append({
                    'title': data['title'],
                    'description': data['description'],
                    'path': data['path']
                })
            except json.JSONDecodeError as e:
                print(f"Error: Failed to parse {template_json_path}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Error reading {template_json_path}: {e}", file=sys.stderr)
    
    return templates


def generate_template_cards(templates):
    """Generate the HTML for template cards"""
    cards = []
    for template in templates:
        card = f"""      <a href="{escape_html(template['path'])}" class="template-card">
        <h2>{escape_html(template['title'])}</h2>
        <p>{escape_html(template['description'])}</p>
        <span class="view-button">View Template →</span>
      </a>"""
        cards.append(card)
    
    return '\n\n'.join(cards)


def generate_index_html(templates):
    """Generate the full index.html content"""
    template_cards = generate_template_cards(templates)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>HTML Templates - Collection</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      background: #ffffff;
      min-height: 100vh;
      padding: 60px 20px;
      color: #1a1a1a;
    }}

    .container {{
      max-width: 1000px;
      width: 100%;
      margin: 0 auto;
    }}

    .header {{
      margin-bottom: 60px;
    }}

    .header h1 {{
      font-size: 2.5rem;
      margin-bottom: 12px;
      font-weight: 600;
      color: #1a1a1a;
      letter-spacing: -0.5px;
    }}

    .header p {{
      font-size: 1.125rem;
      color: #666;
      line-height: 1.6;
    }}

    .templates-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 30px;
      margin-bottom: 30px;
    }}

    .template-card {{
      background: #ffffff;
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      padding: 32px;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      text-decoration: none;
      color: inherit;
      display: block;
    }}

    .template-card:hover {{
      border-color: #1a1a1a;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }}

    .template-card h2 {{
      color: #1a1a1a;
      font-size: 1.5rem;
      margin-bottom: 12px;
      font-weight: 600;
    }}

    .template-card p {{
      color: #666;
      font-size: 0.9375rem;
      line-height: 1.6;
      margin-bottom: 20px;
    }}

    .template-card .view-button {{
      display: inline-block;
      color: #1a1a1a;
      font-size: 0.9375rem;
      font-weight: 500;
      transition: opacity 0.2s ease;
    }}

    .template-card:hover .view-button {{
      opacity: 0.7;
    }}

    .footer {{
      text-align: center;
      color: #666;
      margin-top: 80px;
      font-size: 0.875rem;
    }}

    .footer a {{
      color: #1a1a1a;
      text-decoration: none;
      border-bottom: 1px solid #1a1a1a;
    }}

    .footer a:hover {{
      opacity: 0.7;
    }}

    @media (max-width: 768px) {{
      .header h1 {{
        font-size: 2rem;
      }}

      .header p {{
        font-size: 1rem;
      }}

      .templates-grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <h1>HTML Templates</h1>
      <p>A collection of clean, ready-to-use HTML templates</p>
    </header>

    <div class="templates-grid">
{template_cards}
    </div>

    <footer class="footer">
      <p>
        View this project on 
        <a href="https://github.com/peteralieber/html-templates" target="_blank" rel="noopener noreferrer">GitHub</a>
      </p>
    </footer>
  </div>
</body>
</html>
"""


def main():
    """Main execution"""
    print('Scanning for templates...')
    templates = find_templates()
    
    print(f'Found {len(templates)} template(s):')
    for template in templates:
        print(f"  - {template['title']}")
    
    if len(templates) == 0:
        print('Warning: No templates found. Make sure subdirectories have template.json files.', file=sys.stderr)
        return
    
    print('\nGenerating index.html...')
    html = generate_index_html(templates)
    
    index_path = Path(__file__).parent / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print('✓ index.html generated successfully!')


if __name__ == '__main__':
    main()
