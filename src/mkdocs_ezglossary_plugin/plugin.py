import logging
import re
import os
from html import parser

from mkdocs.plugins import BasePlugin, event_priority
from mkdocs import config
from mkdocs.config import config_options as co

from .glossary import Glossary, get_id

from . import template

log = logging.getLogger("mkdocs.plugins.ezglossary")


class __re:
    def __init__(self):
        self.ws = r"[\n ]*"
        self.section = r"([^:<>\"\|/\@&#][^:<>\"\|/\@]*)"
        self.term = self.section
        self.text = r"([^>]+)"
        self.dt = rf"<dt>(<.*>)?{self.section}:{self.term}(<.*>)?<\/dt>"
        self.dt_default = rf"<dt>(<.*>)?{self.term}(<.*>)?<\/dt>"
        self.dd = r"<dd>\n?((.|\n)+?)<\/dd>"
        self.options = r"([\\\|\=\w\+]+)"


_re = __re()


class GlossaryConfig(config.base.Config):
    tooltip = config.config_options.Choice(('none', 'short', 'full'), default="none")
    inline_refs = config.config_options.Choice(('none', 'short', 'list'), default="none")
    plurals = config.config_options.Choice(('none', 'en', 'inflect'), default="none")
    sections = co.ListOfItems(config.config_options.Type(str), default=[])
    section_config = co.ListOfItems(config.config_options.Type(dict), default=[])
    strict = config.config_options.Type(bool, default=False)
    ignore_case = config.config_options.Type(bool, default=False)
    markdown_links = config.config_options.Type(bool, default=False)
    list_references = config.config_options.Type(bool, default=True)
    list_definitions = config.config_options.Type(bool, default=True)
    use_default = config.config_options.Type(bool, default=False)
    templates = config.config_options.Type(str, default="")
    exclude_from_search = config.config_options.Type(bool, default=False)


class GlossaryPlugin(BasePlugin[GlossaryConfig]):
    def __init__(self):
        self._uuid = "6251a85a-47d0-11ee-be56-0242ac120002"
        self._reflink = "886d7696-137e-4a59-a39d-6f7d311d5bd1"

    def _is_print_site_enabled(self, config):
        """Check if print-site plugin is enabled in the MkDocs configuration."""
        valid_plugin_names = {'print-site', 'mkdocs-print-site-plugin'}
        plugins = config.get('plugins', [])
        
        for plugin_config in plugins:
            plugin_name = None
            if isinstance(plugin_config, dict):
                plugin_name = next(iter(plugin_config.keys()), None)
            elif hasattr(plugin_config, 'name'):
                plugin_name = plugin_config.name
            elif isinstance(plugin_config, str):
                plugin_name = plugin_config
                
            if plugin_name in valid_plugin_names:
                return True
        return False

    def on_pre_build(self, config, **kwargs):
        self._glossary = Glossary(self.config.ignore_case, self.config.plurals)
        if self.config.strict and "_" not in self.config.sections:
            self.config.sections.append("_")
        if self.config.strict and len(self.config.sections) == 0:
            log.error("ezglossary: no sections defined, but 'strict' is true, plugin disabled")
        self._glossary.clear()

    def on_page_markdown(self, content, page, config, files):
        attributes = page.meta

        def _get_definition(anchor):
            anchors = attributes.get('anchors')
            if anchors:
                for anchor_def in anchors:
                    if anchor in anchor_def:
                        return anchor_def[anchor]
            if 'subtitle' in attributes:
                return attributes['subtitle']
            return page.title

        def _add2section(section, term, anchor=None):
            if not anchor:
                if "#" in term:
                    (term, anchor) = term.split("#")
                else:
                    (term, anchor) = (term, "")
            definition = _get_definition(anchor)
            log.debug(f"add2section: {section}:{term}:{anchor} -> '{definition}'")
            self._glossary.add(section,
                               term,
                               'defs',
                               page,
                               definition,
                               anchor)

        ez = attributes.get('terms')
        log.debug(ez)
        if not ez:
            return content

        for entry in ez:
            if isinstance(entry, str):
                _add2section("_", entry)
                continue

            for (section, data) in entry.items():
                if isinstance(data, str):
                    _add2section(section, data)
                    continue

                for term in data:
                    if isinstance(term, str):
                        _add2section(section, term)
                    if isinstance(term, dict):
                        for term, anchor in term.items():
                            _add2section(section, term, anchor)
        return content

    @event_priority(5000)
    def on_page_content(self, content, page, config, files):
        content = self._find_definitions(content, page)
        content = self._register_glossary_links(content, page)
        
        # Apply UUID replacement for print-site compatibility
        _dir = os.path.dirname(page.url) 
        levels = len(_dir.split("/"))
        root = "./" * levels if page.canonical_url and page.canonical_url.replace(config.site_url or "", "").lstrip("/").count("/") < 1 else "../" * levels
        content = self._replace_glossary_links(content, page, root)
        
        return content

    def on_post_page(self, output, page, config):
        _dir = os.path.dirname(page.url)
        levels = len(_dir.split("/"))
        root = "./" * levels if page.canonical_url and page.canonical_url.replace(config.site_url or "", "").lstrip("/").count("/") < 1 else "../" * levels
        
        output = self._replace_inline_refs(output, page, root)
        output = self._print_glossary(output, root, None)
        return output

    def _print_glossary(self, html, root, config=None):
        def _replace(mo):
            types = []
            section = mo.group(1)
            options = mo.group(2) or ""

            lr = "do_refs" in options
            if "no_refs" not in options and "do_refs" not in options:
                lr = self._get_config(section, 'list_references')
            if lr:
                types.append('refs')

            ld = "do_defs" in options
            if "no_defs" not in options and "do_defs" not in options:
                ld = self._get_config(section, 'list_definitions')
            if ld:
                types.append('defs')

            if len(types) == 0:
                log.warning("list_definitons and list_references disabled, summary will be empty")

            if not self._glossary.has(section=section):
                log.warning(f"no section '{section}' found in glossary")

            terms = self._glossary.terms(section)
            theme = ""
            for option in options.replace("\\|", "|").split("|"):
                if "theme" in option:
                    theme = "-" + option.split("=")[1]
            rendered_content = template.render(f"summary{theme}.html",
                                               self.config,
                                               glossary=self._glossary,
                                               types=types,
                                               section=section,
                                               terms=terms,
                                               root=root)
            
            return rendered_content

        # Handle both self-closing and opening/closing tag patterns
        html = re.sub(rf"<glossary::{_re.section}\\?\|?{_re.options}?>", _replace, html)
        html = re.sub(rf"</glossary::[^>]*>", '', html)  # Remove closing tags
        return html

    def _replace_glossary_links(self, output, page, root, config=None):
        """ Search for links to glossary entries detected and marked
            in the first stage and replace them with an actual html
            link pointing to that glossary definition.
        """
        def _replace(mo):
            import html
            id = mo.group(1)
            text = html.unescape(mo.group(2))  # Decode HTML entities

            td = self._glossary.ref_by_id(id)
            text = td.term if text == "__None__" else text
            entry = self._glossary.get_best_definition(td.section, td.term)
            
            if entry is None:
                log.warning(f"page '{page.url}' refers to undefined glossary entry {td.section}:{td.term}")
                term = "" if td.term == "__None__" else td.term
                text = "" if text == "__None__" else text
                sec = f"{td.section}:" if td.section != "_" else ""
                return f'<a href="{sec}{term}">{text}</a>'

            # Apply tooltip configuration logic during link rendering
            if self.config.tooltip == "none":
                # Page references always show title even when tooltip is "none"
                tooltip_text = entry.definition if hasattr(entry, 'page') and (entry.definition == entry.page.title or 'subtitle' in str(entry.definition)) else ""
            elif self.config.tooltip == "short":
                # Sentence-based splitting with fallback to line-based
                if '. ' in entry.definition:
                    sentences = entry.definition.split('. ')
                    tooltip_text = sentences[0] + ('.' if len(sentences) > 1 and not sentences[0].endswith('.') else '')
                else:
                    tooltip_text = entry.definition.split("\n")[0]
            else:  # self.config.tooltip == "full"
                tooltip_text = entry.definition
            
            # Clean tooltip text
            tooltip_text = _html2text(_preserve_visible_text_for_tooltip(tooltip_text))

            # Use anchor-only links for print/PDF output
            href = f"#{entry.target}" if config and self._is_print_site_enabled(config) else f"{root}{entry.page.url}#{entry.target}"

            return f'<a class="mkdocs-ezglossary-link" id="{id}" title="{tooltip_text}" name="{entry.section}:{entry.term}" href="{href}">{text}</a>'
                
        # Try both regex patterns to handle both HTML entity encoded and raw formats
        # Check for HTML entity encoded format first
        regex_entities = fr"{self._uuid}:([a-f0-9]{{32}}):&lt;([^&]*)&gt;"
        regex_original = fr"{self._uuid}:([a-f0-9]{{32}}):<([^>]*)>"
            
        # Test which pattern has matches
        if re.search(regex_entities, output):
            regex = regex_entities
        else:
            regex = regex_original
            
        result = re.sub(regex, _replace, output)
            
        return result

    def _replace_inline_refs_in_content(self, content, page, root):
        """
        Replace inline_refs UUIDs in markdown content for PDF/print compatibility.
        This is similar to _replace_inline_refs but works on content instead of HTML output.
        """
        def _replace(mo):
            section = mo.group(1)
            term = mo.group(2)
            log.debug(f"inline_refs: looking up: '{section}/{term}' in content")

            mode = self._get_config(section, 'inline_refs')

            entries = self._glossary.get(section, term, 'refs')
            # For content processing, we need to return markdown/text instead of HTML
            if mode == 'list':
                if entries:
                    # Create a simple text list for markdown content
                    ref_list = []
                    for entry in entries:
                        if hasattr(entry, 'page') and hasattr(entry.page, 'title'):
                            ref_list.append(f"[{entry.page.title}]({root}{entry.page.url})")
                    return f"Referenced in: {', '.join(ref_list)}"
                else:
                    return ""
            else:
                # For other modes, just remove the UUID placeholder
                return ""

        regex = fr"{self._reflink}:{_re.section}:{_re.term}"
        return re.sub(regex, _replace, content)

    def _replace_inline_refs(self, output, page, root):
        def _replace(mo):
            section = mo.group(1)
            term = mo.group(2)
            log.debug(f"inline_refs: looking up: '{section}/{term}'")

            mode = self._get_config(section, 'inline_refs')

            entries = self._glossary.get(section, term, 'refs')
            return template.render(f"refs-{mode}.html",
                                   self.config,
                                   entries=entries,
                                   root=root)

        regex = fr"{self._reflink}:{_re.section}:{_re.term}"
        return re.sub(regex, _replace, output)

    def _register_glossary_links(self, output, page):

        def _add_link(section, term, text):
            section = "_" if (section == "default" or section is None) else section
            term = term if term else "__None__"
            text = text if text else "__None__"
            log.debug(f"glossary: found link: {section}/{term}/{text}")
            id =self._glossary.add(section, term, 'refs', page)
            return f"{self._uuid}:{id}:<{text}>"

        def _replace(mo):
            return _add_link(mo.group(1), mo.group(2), mo.group(4))

        def _replace_default(mo):
            return _add_link(None, mo.group(1), mo.group(3))

        def _replace_href(mo):
            return _add_link(mo.group(2), mo.group(3), mo.group(4))

        regex = rf"<{_re.section}\:{_re.term}(\\?\|({_re.text}))?>"
        output = re.sub(regex, _replace, output)
        regex = rf"<{_re.term}:(\\?\|({_re.text}))?>"
        output = re.sub(regex, _replace_default, output)

        if self.config.markdown_links:
            regex = rf'<a href="({_re.section}\:)?{_re.term}">({_re.text})?</a>'
            output = re.sub(regex, _replace_href, output)

        return output

    def _find_definitions(self, content, page):
        log.debug(f"_find_definitions({page})")

        def _add_entry(section, term, definition, fmt_pre, fmt_post):
            log.debug(f"glossary: found definition: {section}:{term}:{definition} {fmt_pre}:{fmt_post}")

            if section not in self.config.sections and self.config.strict:
                log.warning(f"ignoring undefined section '{section}' in glossary")
                return None

            # Store the full definition in the glossary
            # Tooltip logic is applied during link rendering in _replace_glossary_links
            _id = self._glossary.add(section, term, 'defs', page, definition)

            inline_refs = self._get_config(section, 'inline_refs')
            reflink = f"\n{self._reflink}:{section}:{term}" if inline_refs != "none" else ""
            return template.render("definition.html",
                                   self.config,
                                   target=_id,
                                   term=term,
                                   definition=definition,
                                   reflink=reflink,
                                   fmt_pre=fmt_pre if fmt_pre else "",
                                   fmt_post=fmt_post if fmt_post else "")

        def _replace(mo):
            fmt_pre = mo.group(1)
            section = mo.group(2)
            term = mo.group(3)
            fmt_post = mo.group(4)
            definition = mo.group(5)
            rendered = _add_entry(section, term, definition, fmt_pre, fmt_post)
            return rendered if rendered else mo.group()

        def _replace_default(mo):
            section = "_"
            fmt_pre = mo.group(1)
            term = mo.group(2)
            fmt_post = mo.group(3)
            definition = mo.group(4)
            rendered = _add_entry(section, term, definition, fmt_pre, fmt_post)
            return rendered if rendered else mo.group()

        if self.config.use_default:
            regex_dt = re.compile(rf"{_re.dt_default}{_re.ws}{_re.dd}", re.MULTILINE)
            content = re.sub(regex_dt, _replace_default, content)

        regex_dt = re.compile(rf"{_re.dt}{_re.ws}{_re.dd}", re.MULTILINE)
        ret = re.sub(regex_dt, _replace, content)
        return ret

    def _get_section_config(self, section):
        for entry in self.config.section_config:
            if entry['name'] == section:
                return entry
        return None

    def _get_config(self, section, entry):
        cfg = self._get_section_config(section)
        if not cfg or entry not in cfg:
            ret = self.config[entry]
        else:
            ret = cfg[entry]
        log.debug(f"_get_config({section}, {entry}): {ret}")
        return ret

    def on_config(self, config: co.Config) -> dict:
        """Process the configuration."""
        # Initialize glossary with current config
        self._glossary = Glossary(
            ignore_case=self.config.ignore_case,
            plurals=self.config.plurals
        )

        # Make templates path relative to the config file directory
        if self.config.templates:
            config_dir = os.path.dirname(config['config_file_path'])
            self.config.templates = os.path.normpath(
                os.path.join(config_dir, self.config.templates)
            )

        return config

    def _get_glossary_pages(self):
        """Extract glossary page URLs from all glossary entries."""
        glossary_pages = set()
        
        def _normalize_page_url(page_url):
            """Convert page URL to .html format."""
            if page_url.endswith('/'):
                return page_url[:-1] + '.html'
            elif page_url.endswith('.md'):
                return page_url[:-3] + '.html'
            elif not page_url.endswith('.html'):
                return page_url + '.html'
            return page_url
        
        # Try direct access to _sections if available
        if hasattr(self._glossary, '_sections'):
            for section_data in self._glossary._sections.values():
                for term_data in section_data.values():
                    for entry in term_data.get('defs', []):
                        if hasattr(entry, 'page') and hasattr(entry.page, 'url'):
                            glossary_pages.add(_normalize_page_url(entry.page.url))
        else:
            # Fallback: use public API
            try:
                sections = getattr(self.config, 'sections', []) or ['_']
                for section in sections:
                    if self._glossary.has(section=section):
                        for term in self._glossary.terms(section):
                            for entry in self._glossary.get(section, term, 'defs'):
                                if hasattr(entry, 'page') and hasattr(entry.page, 'url'):
                                    glossary_pages.add(_normalize_page_url(entry.page.url))
            except Exception as e:
                log.warning(f"Could not determine glossary pages dynamically: {e}")
        
        return glossary_pages

    def _get_glossary_pages_with_sections(self):
        """Extract glossary page URLs mapped to their sections."""
        page_to_sections = {}
        
        def _normalize_page_url(page_url):
            """Convert page URL to .html format."""
            if page_url.endswith('/'):
                return page_url[:-1] + '.html'
            elif page_url.endswith('.md'):
                return page_url[:-3] + '.html'
            elif not page_url.endswith('.html'):
                return page_url + '.html'
            return page_url
        
        # Try direct access to _sections if available
        if hasattr(self._glossary, '_sections'):
            for section_name, section_data in self._glossary._sections.items():
                for term_data in section_data.values():
                    for entry in term_data.get('defs', []):
                        if hasattr(entry, 'page') and hasattr(entry.page, 'url'):
                            page_url = _normalize_page_url(entry.page.url)
                            if page_url not in page_to_sections:
                                page_to_sections[page_url] = set()
                            page_to_sections[page_url].add(section_name)
        else:
            # Fallback: use public API
            try:
                sections = getattr(self.config, 'sections', []) or ['_']
                for section in sections:
                    if self._glossary.has(section=section):
                        for term in self._glossary.terms(section):
                            for entry in self._glossary.get(section, term, 'defs'):
                                if hasattr(entry, 'page') and hasattr(entry.page, 'url'):
                                    page_url = _normalize_page_url(entry.page.url)
                                    if page_url not in page_to_sections:
                                        page_to_sections[page_url] = set()
                                    page_to_sections[page_url].add(section)
            except Exception as e:
                log.warning(f"Could not determine glossary pages dynamically: {e}")
        
        return page_to_sections

    def _filter_excluded_sections_from_text(self, text, excluded_sections):
        """Filter out glossary terms from excluded sections while preserving other content.
        
        This method works generically with any glossary content by:
        1. Identifying terms that belong to excluded sections using the glossary data structure
        2. Finding those terms and their definitions in the search text
        3. Removing the matching patterns while preserving other content
        """
        if not excluded_sections:
            return text
        
        filtered_text = text
        excluded_patterns = []
        
        # Build list of terms from excluded sections using glossary data
        try:
            # Method 1: Direct access to internal structure (more efficient)
            if hasattr(self._glossary, '_sections'):
                for section_name in excluded_sections:
                    if section_name in self._glossary._sections:
                        section_data = self._glossary._sections[section_name]
                        for term_name, term_data in section_data.items():
                            for entry in term_data.get('defs', []):
                                if hasattr(entry, 'term'):
                                    term = entry.term.strip()
                                    # Build pattern: "term definition_text"
                                    # The search index format is: "term Has definition here.  next_term"
                                    escaped_term = re.escape(term)
                                    # Match term followed by content until period + spaces (more robust)
                                    pattern = rf'\b{escaped_term}\b[^.]*?\.\s*'
                                    excluded_patterns.append(pattern)
            else:
                # Method 2: Fallback using public API
                for section in excluded_sections:
                    if self._glossary.has(section=section):
                        for term in self._glossary.terms(section):
                            entries = self._glossary.get(section, term, 'defs')
                            for entry in entries:
                                if hasattr(entry, 'term'):
                                    term = entry.term.strip()
                                    escaped_term = re.escape(term)
                                    pattern = rf'\b{escaped_term}\b[^.]*?\.\s*'
                                    excluded_patterns.append(pattern)
                                    
        except Exception as e:
            log.warning(f"Could not build exclusion patterns for sections {excluded_sections}: {e}")
            return text
        
        # Apply exclusion patterns
        for pattern in excluded_patterns:
            try:
                old_length = len(filtered_text)
                filtered_text = re.sub(pattern, '', filtered_text, flags=re.IGNORECASE)
                if len(filtered_text) < old_length:
                    removed = old_length - len(filtered_text)
                    log.debug(f"Excluded {removed} characters using pattern: {pattern[:50]}...")
            except re.error as e:
                log.warning(f"Invalid regex pattern {pattern}: {e}")
                continue
        
        # Clean up extra whitespace
        filtered_text = re.sub(r'\s+', ' ', filtered_text).strip()
        
        return filtered_text

    def _process_print_page(self, site_dir, config):
        """Process print_page.html for print-site compatibility."""
        print_page_path = os.path.join(site_dir, 'print_page.html')
        if not os.path.exists(print_page_path):
            return
            
        try:
            with open(print_page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            class DummyPage:
                url = "print_page.html"
            
            content = self._replace_glossary_links(content, DummyPage(), "./", config)
            content = self._replace_inline_refs(content, DummyPage(), "./")
            processed_content = self._print_glossary(content, "./", config)
            
            # Convert glossary page links to anchor-only links
            for page_url in self._get_glossary_pages():
                page_filename = page_url.split('/')[-1]
                pattern = fr'href="[^"]*{re.escape(page_filename)}#([^"]*)"'
                processed_content = re.sub(pattern, r'href="#\1"', processed_content)
            
            # Handle any remaining 32-character hex anchors
            processed_content = re.sub(r'href="[^"]*#([a-f0-9]{32})"', r'href="#\1"', processed_content)
            
            if processed_content != content:
                with open(print_page_path, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                log.info("Processed glossary tags and converted links in print_page.html")
                
        except Exception as e:
            log.warning(f"Failed to process print_page.html: {e}")

    def _clean_search_index(self, site_dir):
        """Clean UUID placeholders from search index."""
        import json
        
        search_index_path = os.path.join(site_dir, 'search', 'search_index.json')
        if not os.path.exists(search_index_path):
            return
            
        try:
            with open(search_index_path, 'r', encoding='utf-8') as f:
                search_data = json.load(f)
            
            # Get mapping of pages to their sections for section-specific exclude_from_search
            page_to_sections = self._get_glossary_pages_with_sections()
            
            # Check if any section has exclude_from_search enabled
            any_exclude_from_search = False
            if self.config.exclude_from_search:
                any_exclude_from_search = True
            else:
                # Check section-specific configs
                sections = getattr(self.config, 'sections', []) or ['_']
                for section in sections:
                    if self._get_config(section, 'exclude_from_search'):
                        any_exclude_from_search = True
                        break
            
            if any_exclude_from_search and page_to_sections:
                log.info(f"Checking glossary content exclusion from search for pages: {set(page_to_sections.keys())}")
            
            main_uuid_pattern = re.compile(fr"{re.escape(self._uuid)}:[a-f0-9]{{32}}:<[^>]*>")
            reflink_uuid_pattern = re.compile(fr"{re.escape(self._reflink)}:[^:\s]*:[^:\s]*")
            
            modified = False
            for doc in search_data.get('docs', []):
                # Clean UUIDs from title
                if doc.get('title'):
                    original = doc['title']
                    doc['title'] = reflink_uuid_pattern.sub('', main_uuid_pattern.sub('', original)).strip()
                    if doc['title'] != original:
                        modified = True
                
                # Handle text content with section-specific exclusions
                if doc.get('text'):
                    original = doc['text']
                    
                    # Check if this is a glossary page that needs section filtering
                    if page_to_sections and doc.get('location'):
                        doc_location = doc['location']
                        base_location = doc_location.split('#')[0]
                        
                        if base_location.endswith('/'):
                            base_location = base_location[:-1] + '.html'
                        elif not base_location.endswith('.html'):
                            base_location = base_location + '.html'
                        
                        if base_location in page_to_sections:
                            page_sections = page_to_sections[base_location]
                            
                            # Check global exclude_from_search first
                            if self.config.exclude_from_search:
                                # Global exclusion - remove all content
                                doc['text'] = ""
                                modified = True
                                continue
                            else:
                                # Check for section-specific exclusions
                                excluded_sections = []
                                for section in page_sections:
                                    if self._get_config(section, 'exclude_from_search'):
                                        excluded_sections.append(section)
                                
                                if excluded_sections:
                                    # Filter out content from excluded sections
                                    filtered_text = self._filter_excluded_sections_from_text(original, excluded_sections)
                                    doc['text'] = reflink_uuid_pattern.sub('', main_uuid_pattern.sub('', filtered_text)).strip()
                                    if excluded_sections:
                                        log.info(f"Filtered sections {excluded_sections} from search content for {doc.get('location', 'unknown')}")
                                    modified = True
                                    continue
                    
                    # Default: just clean UUIDs
                    doc['text'] = reflink_uuid_pattern.sub('', main_uuid_pattern.sub('', original)).strip()
                    if doc['text'] != original:
                        modified = True
            
            if modified:
                with open(search_index_path, 'w', encoding='utf-8') as f:
                    json.dump(search_data, f, ensure_ascii=False, separators=(',', ':'))
                log.info("Cleaned UUIDs and processed glossary content in search index")
                    
        except Exception as e:
            log.warning(f"Failed to clean UUIDs from search index: {e}")

    def on_post_build(self, config, **kwargs):
        """Clean UUID placeholders from print pages and search index after build completion"""
        site_dir = config['site_dir']
        self._process_print_page(site_dir, config)
        self._clean_search_index(site_dir)


def _preserve_visible_text_for_tooltip(s: str) -> str:
    """
    Normalize nested glossary/HTML constructs to *visible text* only, so that
    _html2text() receives the intended words for tooltip rendering.

    Args:
        s (str): The input string containing glossary/HTML constructs.

    Returns:
    # Keep anchor text, drop the tag.
    # Note: This regex does not handle nested anchor tags, but nested <a> elements are invalid in HTML and not expected in glossary definitions.
    s = re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', s, flags=re.IGNORECASE | re.DOTALL)
      - <name:TERM>               -> TERM
      - &lt;name:TERM&gt;         -> TERM
      - <name:>                   -> name
      - <a ...>TEXT</a>           -> TEXT
    """
    # Keep anchor text, drop the tag
    s = re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', s, flags=re.IGNORECASE | re.DOTALL)
    # Glossary markers to plain text (escaped/raw/name-only)
    s = re.sub(r'&lt;([A-Za-z0-9_-]+):([^><|]+)&gt;', r'\2', s)
    s = re.sub(r'<([A-Za-z0-9_-]+):([^><|]+)>', r'\2', s)
    s = re.sub(r'<([A-Za-z0-9_-]+):>', r'\1', s)
    return s


def _html2text(content):
    class HTMLFilter(parser.HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = ""

        def handle_data(self, data):
            self.text += data

    f = HTMLFilter()
    f.feed(content)
    return f.text.strip()
