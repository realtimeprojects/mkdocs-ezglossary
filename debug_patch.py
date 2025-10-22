import sys

# Read the entire file
with open('src/mkdocs_ezglossary_plugin/plugin.py', 'r') as f:
    content = f.read()

# Add logging import at the top if not present
if "import logging" not in content:
    content = content.replace(
        "import os",
        "import os\nimport logging"
    )

# Add logging to our on_page_context method
old_method = '''    def on_page_context(self, context, page, config, nav):
        """
        Clean up UUID placeholders from page content before search indexing.
        
        This ensures the search plugin indexes clean content without UUID placeholders
        that would otherwise appear in search results.
        """
        if hasattr(page, 'content') and page.content:
            # Calculate root path for this page (same logic as on_post_page)
            _dir = os.path.dirname(page.url)
            levels = len(_dir.split("/"))
            if page.canonical_url and page.canonical_url.replace(config.site_url or "", "").lstrip("/").count("/") < 1:
                root = "./" * levels
            else:
                root = "../" * levels
            
            # Clean the page content of UUID placeholders before search indexing
            page.content = self._replace_glossary_links(page.content, page, root)
        
        return context'''

new_method = '''    def on_page_context(self, context, page, config, nav):
        """
        Clean up UUID placeholders from page content before search indexing.
        
        This ensures the search plugin indexes clean content without UUID placeholders
        that would otherwise appear in search results.
        """
        log = logging.getLogger("mkdocs.plugins.ezglossary")
        
        if hasattr(page, 'content') and page.content:
            log.info(f"Processing page context for: {page.url}")
            
            # Check if content has UUIDs before processing
            uuid_count_before = page.content.count(self._uuid)
            log.info(f"UUID count before cleaning: {uuid_count_before}")
            
            # Calculate root path for this page (same logic as on_post_page)
            _dir = os.path.dirname(page.url)
            levels = len(_dir.split("/"))
            if page.canonical_url and page.canonical_url.replace(config.site_url or "", "").lstrip("/").count("/") < 1:
                root = "./" * levels
            else:
                root = "../" * levels
            
            # Clean the page content of UUID placeholders before search indexing
            page.content = self._replace_glossary_links(page.content, page, root)
            
            # Check if content has UUIDs after processing
            uuid_count_after = page.content.count(self._uuid)
            log.info(f"UUID count after cleaning: {uuid_count_after}")
        
        return context'''

# Replace the method
content = content.replace(old_method, new_method)

# Write the modified file
with open('src/mkdocs_ezglossary_plugin/plugin.py', 'w') as f:
    f.write(content)

print("Added debug logging to on_page_context method")
