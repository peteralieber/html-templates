require 'json'

module Jekyll
  class TemplateGenerator < Generator
    safe true
    priority :high

    def generate(site)
      templates = []

      # Scan all directories in the root for template.json files
      Dir.glob(File.join(site.source, '*/')).each do |dir|
        next if File.basename(dir).start_with?('_', '.')
        
        template_json = File.join(dir, 'template.json')
        
        if File.exist?(template_json)
          begin
            data = JSON.parse(File.read(template_json))
            
            # Validate required fields
            if data['title'] && data['description'] && data['path']
              # Validate path is safe (relative, no .., no external URLs)
              path = data['path']
              if !path.start_with?('/') && !path.include?('..') && !path.match?(/^[a-z]+:\/\//i)
                templates << {
                  'title' => data['title'],
                  'description' => data['description'],
                  'path' => data['path'],
                  'directory' => File.basename(dir)
                }
              else
                Jekyll.logger.warn "TemplateGenerator:", "Skipping #{template_json}: invalid path"
              end
            else
              Jekyll.logger.warn "TemplateGenerator:", "Skipping #{template_json}: missing required fields"
            end
          rescue JSON::ParserError => e
            Jekyll.logger.error "TemplateGenerator:", "Failed to parse #{template_json}: #{e.message}"
          end
        end
      end

      # Sort templates alphabetically by title
      templates.sort_by! { |t| t['title'] }

      # Make templates available to Jekyll
      site.data['templates'] = templates
      
      Jekyll.logger.info "TemplateGenerator:", "Found #{templates.length} template(s)"
    end
  end
end
