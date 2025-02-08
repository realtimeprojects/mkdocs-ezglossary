import logging

from yaxp import xpath as xp

from mkdocs_ezglossary_plugin.glossary import get_id, Glossary


log = logging.getLogger(__name__)

def has_link(page, 
             section: str, 
             term: str, 
             title: str, 
             href: str, 
             text: str, 
             destination: str = None,
             index: int = 0,
             is_page_ref: bool = False) -> bool:
    """Check if a page contains a glossary link with the specified attributes.
    
    Args:
        page: The page HTML to check
        section: The glossary section
        term: The term to look for (source term)
        title: Expected title attribute
        href: Expected base href (e.g., "../simple.md")
        text: Expected link text
        destination: The term being linked to (defaults to term if not specified)
        index: Index of the reference (default: 0)
    
    Returns:
        bool: True if the link exists with all specified attributes
    """
    # Use destination term if provided, otherwise use source term
    dest_term = destination if destination is not None else term
    
    # Get IDs for both the reference and the definition
    ref_id = get_id(section, term, "refs", index)
    log.debug(f"ref_id: {ref_id} for {section}:{term}, refs, {index}")
    def_id = "" if is_page_ref else get_id(section, dest_term, "defs", 0)
    get_id(section, dest_term, "defs", 0)
    log.debug(f"def_id: {def_id} for {section}:{term} -> {dest_term}, defs, 0")
    
    full_href = f"{href}#{def_id}"
    
    # Build link attributes
    attrs = {
        "_class": "mkdocs-ezglossary-link",
        "id": ref_id,
        "href": full_href,
        "text": text
    }
    if title:
        attrs["title"] = "*" + title

    link = xp.a(**attrs)
    xpath_str = str(link)
    
    log.warning(f"Looking for link with xpath: {xpath_str}")
    log.warning(f"Expected ref_id: {ref_id}")
    log.warning(f"Expected href: {full_href}")
    
    # Get all links and log them
    all_links = page.xpath("//a[@class='mkdocs-ezglossary-link']")
    log.warning(f"Found {len(all_links)} glossary links in document:")
    for l in all_links:
        log.warning(f"Link: id='{l.get('id')}' href='{l.get('href')}' text='{l.text}' title='{l.get('title')}'")
    
    result = len(page.xpath(xpath_str)) == 1
    log.warning(f"Match result: {result}")
    
    return result

def has_definition(page, section: str, term: str, definition: str, index: int = 0) -> bool:
    """Check if a page contains a term definition with the specified attributes.
    
    Args:
        page: The page HTML to check
        section: The glossary section
        term: The term to look for
        definition: Expected definition text
        index: Index of the definition (default: 0)
    
    Returns:
        bool: True if the definition exists with all specified attributes
    """
    dl = xp.dl
    dl = dl.has(xp.dt.has(xp.a(id=get_id(section, term, "defs", index), text=term)))
    dl = dl.has(xp.dd(text=definition))
    return len(page.xpath(str(dl))) == 1

def has_summary_entry(page,
                      section: str, 
                      term: str, 
                      href: str = None, 
                      ref_text: str = None):
    """Check if a reference entry exists in the glossary summary."""
    # Create xpath for the dl element with class and id
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id=section)
    
    # Find dt containing the term (case sensitive)
    dt = xp.dt(_="*" + term)
    dl = dl.has(dt)
    
    if href:
        # Calculate the full href with the target id
        full_href = f"{href}#{get_id(section, term.lower(), 'defs', 0)}"
        
        # Find dd containing a link with the exact href and text
        dd = xp.dd.ul.li.a(href=full_href, text=ref_text)
        dl = dl.has(dd)
    else:
        full_href = None
    
    xpath_str = str(dl)
    log.warning(f"Looking for summary entry with xpath: {xpath_str}")
    log.warning(f"Expected section: {section}")
    log.warning(f"Expected term: {term}")
    log.warning(f"Expected href: {full_href}")
    log.warning(f"Expected text: {ref_text}")
    
    # Get all summary entries and log them
    all_entries = page.xpath("//dl[@class='mkdocs-ezglossary-summary']")
    log.warning(f"Found {len(all_entries)} summary sections in document:")
    for entry in all_entries:
        section_id = entry.get('id')
        terms = entry.xpath(".//dt")
        refs = entry.xpath(".//dd//a")
        log.warning(f"Section '{section_id}':")
        for t in terms:
            log.warning(f"  Term: '{t.text.strip()}'")
        for r in refs:
            log.warning(f"  Reference: href='{r.get('href')}' text='{r.text.strip()}'")
    
    result = len(page.xpath(xpath_str)) == 1
    log.warning(f"Match result: {result}")
    
    return result

def has_summary_reference(page, section: str, term: str, ref_href: str, ref_text: str, index: int = 0) -> bool:
    """Check if a summary entry contains a reference with the specified attributes.
    
    Args:
        page: The page HTML to check
        section: The glossary section
        term: The term to look for
        ref_href: Expected reference href
        ref_text: Expected reference text
        index: Index of the reference (default: 0)
    
    Returns:
        bool: True if the summary reference exists with all specified attributes
    """
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id=section)
    dl = dl.has(xp.dt.has(xp.a(text=term)))
    dl = dl.has(xp.dd.ul.li.a(href=ref_href, text=ref_text))
    return len(page.xpath(str(dl))) == 1 