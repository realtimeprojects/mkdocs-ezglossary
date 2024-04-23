import hashlib
import logging
import html

log = logging.getLogger(__name__)


def get_id(section: str, term: str, linktype: str, n: str):
    return str(hashlib.md5(f"{section}_{term}_{linktype}_{n}".encode()).hexdigest())


class Entry:
    """ An entry in the glossary. """

    def __init__(self, target, page, definition):
        self.target = target
        """ The anchor to directly point to this specific link. """

        self.page = page
        """ The url of the page to which this entry points to. """

        self.definition = definition
        """ The definition of the term. """

    def __repr__(self):
        return self.page.url


class Glossary:
    """ The complete glossary for all sections """

    def __init__(self):
        self.clear()

    def add(self, section, term, linktype, page, definition=None, anchor=None):
        term = html.unescape(term.strip())
        log.debug(f"glossary.add({section}, {term}, {linktype}, '{definition}', {anchor})")
        links = self._links(section, term, linktype)
        _id = get_id(section, term, linktype, len(links))
        anchor = _id if anchor is None else anchor
        links[_id] = Entry(anchor, page, definition)
        return _id

    def has(self, section: str) -> bool:
        """ Check if the glossary has a section named **section**.

            Args:
                section:
                    The name of the section to check

            Returns:
                    True, if a section with the given name exists.
        """
        return section in self._glossary

    def get(self, section: str, term: str, linktype: str) -> list[Entry]:
        """ Get a list of [Entry][mkdocs_ezglossary_plugin.glossary.Entry] instances
            for a specific **term** in a **section**.

            Args:
                section:
                    The name of the section
                term:
                    The term for which the [Entry] instances should be retreived.
                linktype:
                    Defines which type of links should be returned.

                    `refs`
                    : returns all references to the term

                    `defs`
                    : returns all definitions for the term

            Returns:
                A list of either `definitions` or `references` for the given term.
        """
        links = self._links(section, html.unescape(term), linktype).values()
        return list(links)

    def definition(self, section: str, term: str) -> str:
        """ Get the definition for a term.

            Args:
                section:
                    The name of the section
                term:
                    The term to get the definition for

            Returns:
                The definition of the term
        """
        defs = self.get(section, html.unescape(term), 'defs')
        if not defs:
            return ""
        return defs[0].definition

    def terms(self, section: str) -> list[str]:
        """ Return a list of entries for a specific section.

            Args:
                section:
                    The name of the section.

            Returns:
                A list of all terms in the specific section.
        """
        keys = list(self._section(section).keys())
        keys.sort()
        return keys

    def clear(self):
        self._glossary = {}

    def _links(self, section, term, linktype):
        return self._term(section, term)[linktype]

    def _term(self, section, term):
        _section = self._section(section)
        if term not in _section:
            self._section(section)[term] = {'defs': {}, 'refs': {}}
        return self._section(section)[term]

    def _section(self, section):
        if section not in self._glossary:
            self._glossary[section] = {}
        return self._glossary[section]
