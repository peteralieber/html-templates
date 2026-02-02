# html-templates
Templates for webpages and websites

## Adding a New Template

To add a new template to this collection:

1. Create a new directory with your template files
2. Add a `template.json` file in the directory with the following structure:
   ```json
   {
     "title": "Your Template Name",
     "description": "A brief description of your template",
     "path": "your-directory/index.html"
   }
   ```
3. Commit and push your changes

The landing page will be automatically built and deployed by GitHub Actions when changes are pushed to the main branch.

## Local Development

This site uses Jekyll to generate the landing page with search functionality.

### Prerequisites

- Ruby 3.x
- Bundler

### Setup

1. Install dependencies:
   ```bash
   bundle install
   ```

2. Build the site:
   ```bash
   bundle exec jekyll build
   ```

3. Serve locally:
   ```bash
   bundle exec jekyll serve
   ```

The site will be available at `http://localhost:4000/`

## Features

- **Automatic template discovery**: Templates are automatically discovered from subdirectories containing `template.json` files
- **Client-side search**: Search templates by name, description, or directory name
- **Responsive design**: Clean, modern interface that works on all devices
- **SEO optimized**: Built-in SEO tags for better search engine visibility
