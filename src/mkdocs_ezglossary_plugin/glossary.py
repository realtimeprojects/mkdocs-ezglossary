import re
import hashlib
import logging
import inflect
from typing import Tuple

from .plurals import plurals

engine = inflect.engine()

log = logging.getLogger(__name__)


def get_id(section: str, term: str, linktype: str, index: int = 0) -> str:
    """Generate a unique ID for a glossary entry.
    
    Args:
        section: The glossary section.
        term: The term.
        linktype: Type of link ('refs' or 'defs').
        index: Index of the entry (only used for 'refs').
    
    Returns:
        str: A unique hash ID, or None if no matching definition exists.
    """
    # For case-insensitive matching, convert to lowercase before hashing
    section = section.lower()
    term = term.lower()
    
    # Base key is always section:term
    key = f"{section}:{term}"
    base_id = hashlib.md5(key.encode()).hexdigest()
    
    # For definitions, just return the base ID
    if linktype == 'defs':
        return base_id
    
    # For references, include the index to make each reference unique
    if linktype == 'refs':
        ref_key = f"{key}:ref:{index}"
        return hashlib.md5(ref_key.encode()).hexdigest()
        
    raise ValueError(f"Invalid linktype: {linktype}")


class Entry:
    """An entry in the glossary."""
    
    def __init__(self, target, page, definition, section, term, ref_id=None):
        self.target = target
        """The anchor to directly point to this specific link."""
        
        self.page = page
        """The URL of the page to which this entry points."""
        
        self.definition = definition
        """The definition of the term."""
        
        self.section = section
        """The section of the term of this entry. (Since v1.7.0a1)"""
        
        self.term = term
        """The term of this entry. (Since v1.7.0a1)"""
        
        self.ref_id = ref_id
        """The ID of the reference link to this entry."""
    
    def __repr__(self):
        """Return a string representation of the entry showing all fields."""
        return (f"Entry(section='{self.section}', term='{self.term}', "
                f"target='{self.target}', page='{self.page}', "
                f"ref_id='{self.ref_id}', definition='{self.definition}')")


class Glossary:
    """The complete glossary for all sections."""
    
    def __init__(self, ignore_case, plurals):
        self.clear()
        self.ignore_case = ignore_case
        self.plurals = plurals
    
    def clear(self):
        """Clear the glossary."""
        # Store sections as: 
        # { section: { 'defs': {term: {id: Entry}}, 'refs': {term: {id: Entry}} } }
        self._glossary = {}
    
    def add(self, section: str, term: str, linktype: str, page: str, definition: str = None, anchor: str = None):
        """Add a new entry to the glossary.
        
        Args:
            section: Section name to add the entry to.
            term: The term (can be plural or singular).
            linktype: Type of entry ('refs' or 'defs').
            page: Page object where the entry is located.
            definition: Optional definition text.
            anchor: Optional anchor ID.
        
        Returns:
            str: The ID of the added entry.
        """
        term = term.strip()
        log.debug(f"glossary.add({section}, {term}, {linktype}, '{definition}', {anchor})")
        
        # Initialize section if needed
        if section not in self._glossary:
            log.debug(f"    adding section: '{section}'")
            self._glossary[section] = {'refs': {}, 'defs': {}}
        
        # Get the appropriate dictionary for this linktype
        links_dict = self._glossary[section][linktype]
        
        # Initialize term entry if needed
        if term not in links_dict:
            links_dict[term] = {}
        
        # Generate IDs
        _id = get_id(section, term, linktype, len(links_dict[term]))
        log.debug(f"    _id: {_id} FOR {section}:{term}:{linktype}:{len(links_dict[term])}")
        
        anchor = _id if anchor is None else anchor
        entry = Entry(anchor, page, definition, section, term, _id)
        links_dict[term][_id] = entry
        log.debug(f"added entry: {entry}")
        
        return _id
    
    def get(self, section: str, term: str, linktype: str) -> list[Entry]:
        """Get all entries for a term, including singular/plural variants.
        
        Args:
            section: Section to search in.
            term: Term to find (can be plural or singular).
            linktype: Type of entries to find ('refs' or 'defs').
        
        Returns:
            list[Entry]: List of matching Entry objects.
        """
        log.debug(f"glossary.get({section}, {term}, {linktype})")
        if section not in self._glossary:
            log.debug(f"    section not in glossary: {section}")
            log.debug(f"    glossary keys: {self._glossary.keys()}")
            return []
        
        results = []
        links_dict = self._glossary[section][linktype]
        found_terms = set()  # Track which terms we've already processed
        
        # Helper to add entries while handling case sensitivity
        def add_entries(search_term):
            if search_term in links_dict and search_term not in found_terms:
                found_terms.add(search_term)
                results.extend(links_dict[search_term].values())
        
        # Handle case sensitivity
        if self.ignore_case:
            term_upper = term.upper()
            for stored_term in links_dict:
                if stored_term.upper() == term_upper:
                    add_entries(stored_term)
        else:
            # Add direct matches only
            add_entries(term)
        
        # Handle plurals
        if self.plurals != 'none':
            variants = self._get_term_variants(term)
            for variant in variants:
                if variant != term:  # Skip original term as it's already been checked
                    if self.ignore_case:
                        variant_upper = variant.upper()
                        for stored_term in links_dict:
                            if stored_term.upper() == variant_upper:
                                add_entries(stored_term)
                    else:
                        add_entries(variant)
        
        return results
    
    def _get_term_variants(self, term: str) -> set[str]:
        """Get all singular/plural variants of a term.
        
        Args:
            term: Term to find variants for.
        
        Returns:
            set[str]: Set of variant terms (including original).
        """
        variants = {term}
        
        if self.plurals == 'inflect':
            try:
                from inflect import engine
                p = engine()
                # Try getting singular if term is plural
                singular = p.singular_noun(term)
                if singular:
                    variants.add(singular)
                else:
                    # Term might be singular, try getting plural
                    variants.add(p.plural_noun(term))
            except ImportError:
                log.warning("inflect library not available")
                return variants
        
        elif self.plurals in plurals:
            term_to_check = term.upper() if self.ignore_case else term
            rules = plurals[self.plurals]
            
            # Try each plural rule
            for ending, replacements in rules.items():
                for replacement in replacements:
                    if self.ignore_case:
                        ending = ending.upper()
                        replacement = replacement.upper()
                    
                    # Always try both directions for each rule
                    # Try converting plural to singular
                    if re.search(ending, term_to_check):
                        singular = re.sub(ending, replacement, term_to_check)
                        variants.add(singular)
                    
                    # Try converting singular to plural
                    if replacement:  # Only if replacement is not empty
                        plural = re.sub(f"{replacement}$", ending.rstrip('$'), term_to_check)
                        variants.add(plural)
                    else:  # For empty replacement, just add 's'
                        plural = term_to_check + ending.rstrip('$')
                        variants.add(plural)
        
        return variants
    
    def has(self, section: str) -> bool:
        """Check if the glossary has a section named **section**.
        
        Args:
            section: The name of the section to check.
        
        Returns:
            bool: True if a section with the given name exists.
        """
        return section in self._glossary
    
    def terms(self, section: str) -> list[str]:
        """Get all terms in a section.
        
        Args:
            section: The name of the section.
        
        Returns:
            list[str]: List of terms in the section.
        """
        if section not in self._glossary:
            return []
        # Combine unique terms from both refs and defs
        terms = set()
        terms.update(self._glossary[section]['defs'].keys())
        
        def update_terms(new_terms):
            for term in new_terms:
                if term not in terms:
                    definition = self.get_best_definition(section, term)
                    if definition and definition.term not in terms:
                        terms.add(definition.term)
        update_terms(self._glossary[section]['refs'].keys())
        
        return sorted(terms)
    
    def definition(self, section: str, term: str) -> str:
        """Get the definition for a term.
        
        Args:
            section: The name of the section.
            term: The term to get the definition for.
        
        Returns:
            str: The definition of the term.
        """
        defs = self.get(section, term, 'defs')
        if not defs:
            return ""
        return defs[0].definition
    
    def get_refs(self, section, term):
        """Get all reference entries for a term.
        
        Args:
            section: The name of the section.
            term: The term to get references for.
        
        Returns:
            list[Entry]: List of reference entries.
        """
        return self.get(section, term, 'refs')
    
    def get_defs(self, section, term):
        """Get all definition entries for a term.
        
        Args:
            section: The name of the section.
            term: The term to get definitions for.
        
        Returns:
            list[Entry]: List of definition entries.
        """
        return self.get(section, term, 'defs')
    
    def ref_by_id(self, id: str) -> Entry:
        """Get a reference entry by its ID.
        
        Args:
            id: The ID of the reference to find.
        
        Returns:
            Entry: The matching reference entry.
        
        Raises:
            KeyError: If no reference with the given ID exists.
        """
        # Search through all sections and terms
        for section in self._glossary.values():
            for term_entries in section['refs'].values():
                for entry_id, entry in term_entries.items():
                    if entry_id == id:
                        return entry
        
        raise KeyError(f"No reference found with ID: {id}")
    
    def get_best_definition(self, section: str, term: str) -> Entry:
        """Get the best matching definition for a term.
        
        Args:
            section: The glossary section.
            term: The base term (usually singular).
        
        Returns:
            Entry: The best matching definition entry, or None if no match found.
        """
        defs = self.get(section, term, 'defs')
        log.debug(f"get_best_definition({section}:{term}): defs: {defs}")
        
        # Try exact match with displayed text first
        if len(defs) > 1:
            log.warning(f"multiple definitions found for <{section}:{term}>, looking for exact match")
            for d in defs:
                log.warning(f"\t{d}")
                if d.term.lower() == term.lower():
                    log.warning(f"\tfound exact match: {d}")
                    return d
            log.warning(f"\tno exact match found, using first definition")
        
        # Fall back to first definition
        if defs:
            return defs[0]
        
        return None
