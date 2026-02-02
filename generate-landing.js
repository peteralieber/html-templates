#!/usr/bin/env node

/**
 * Script to generate the main landing page (index.html) by scanning
 * subdirectories for template.json files.
 */

const fs = require('fs');
const path = require('path');

/**
 * Escape HTML special characters to prevent XSS
 */
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Validate that the path is a safe relative path within the repository
 */
function isValidPath(templatePath) {
  // Must be a relative path (not starting with / or containing ..)
  if (templatePath.startsWith('/') || templatePath.includes('..')) {
    return false;
  }
  // Should not be an external URL
  if (templatePath.match(/^[a-z]+:\/\//i)) {
    return false;
  }
  return true;
}

// Get all subdirectories that contain a template.json file
function findTemplates() {
  const templates = [];
  const rootDir = __dirname;
  
  // Read all items in the root directory
  const items = fs.readdirSync(rootDir, { withFileTypes: true });
  
  // Filter for directories only (exclude hidden directories)
  const directories = items.filter(item => 
    item.isDirectory() && !item.name.startsWith('.')
  );
  
  // Check each directory for template.json
  for (const dir of directories) {
    const templateJsonPath = path.join(rootDir, dir.name, 'template.json');
    
    if (fs.existsSync(templateJsonPath)) {
      try {
        const data = JSON.parse(fs.readFileSync(templateJsonPath, 'utf8'));
        
        // Validate required fields
        if (!data.title || !data.description || !data.path) {
          console.warn(`Skipping ${templateJsonPath}: missing required fields`);
          continue;
        }
        
        // Validate path safety
        if (!isValidPath(data.path)) {
          console.warn(`Skipping ${templateJsonPath}: invalid path "${data.path}"`);
          continue;
        }
        
        templates.push({
          title: data.title,
          description: data.description,
          path: data.path
        });
      } catch (error) {
        console.error(`Error reading ${templateJsonPath}:`, error.message);
      }
    }
  }
  
  return templates;
}

// Generate the HTML for template cards
function generateTemplateCards(templates) {
  return templates.map(template => `      <a href="${escapeHtml(template.path)}" class="template-card">
        <h2>${escapeHtml(template.title)}</h2>
        <p>${escapeHtml(template.description)}</p>
        <span class="view-button">View Template →</span>
      </a>`).join('\n\n');
}

// Generate the full index.html content
function generateIndexHtml(templates) {
  const templateCards = generateTemplateCards(templates);
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>HTML Templates - Collection</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      background: #ffffff;
      min-height: 100vh;
      padding: 60px 20px;
      color: #1a1a1a;
    }

    .container {
      max-width: 1000px;
      width: 100%;
      margin: 0 auto;
    }

    .header {
      margin-bottom: 60px;
    }

    .header h1 {
      font-size: 2.5rem;
      margin-bottom: 12px;
      font-weight: 600;
      color: #1a1a1a;
      letter-spacing: -0.5px;
    }

    .header p {
      font-size: 1.125rem;
      color: #666;
      line-height: 1.6;
    }

    .templates-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 30px;
      margin-bottom: 30px;
    }

    .template-card {
      background: #ffffff;
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      padding: 32px;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      text-decoration: none;
      color: inherit;
      display: block;
    }

    .template-card:hover {
      border-color: #1a1a1a;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .template-card h2 {
      color: #1a1a1a;
      font-size: 1.5rem;
      margin-bottom: 12px;
      font-weight: 600;
    }

    .template-card p {
      color: #666;
      font-size: 0.9375rem;
      line-height: 1.6;
      margin-bottom: 20px;
    }

    .template-card .view-button {
      display: inline-block;
      color: #1a1a1a;
      font-size: 0.9375rem;
      font-weight: 500;
      transition: opacity 0.2s ease;
    }

    .template-card:hover .view-button {
      opacity: 0.7;
    }

    .footer {
      text-align: center;
      color: #666;
      margin-top: 80px;
      font-size: 0.875rem;
    }

    .footer a {
      color: #1a1a1a;
      text-decoration: none;
      border-bottom: 1px solid #1a1a1a;
    }

    .footer a:hover {
      opacity: 0.7;
    }

    @media (max-width: 768px) {
      .header h1 {
        font-size: 2rem;
      }

      .header p {
        font-size: 1rem;
      }

      .templates-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <h1>HTML Templates</h1>
      <p>A collection of clean, ready-to-use HTML templates</p>
    </header>

    <div class="templates-grid">
${templateCards}
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
`;
}

// Main execution
function main() {
  console.log('Scanning for templates...');
  const templates = findTemplates();
  
  console.log(`Found ${templates.length} template(s):`);
  templates.forEach(t => console.log(`  - ${t.title}`));
  
  if (templates.length === 0) {
    console.warn('No templates found. Make sure subdirectories have template.json files.');
    return;
  }
  
  console.log('\nGenerating index.html...');
  const html = generateIndexHtml(templates);
  
  const indexPath = path.join(__dirname, 'index.html');
  fs.writeFileSync(indexPath, html, 'utf8');
  
  console.log('✓ index.html generated successfully!');
}

main();
