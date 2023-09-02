import logging

log = logging.getLogger(__name__)


class Entry:
    """ An entry in the glossary. """

    def __init__(self, target, page, definition):
        self.target = target
        """ The anchor to directly point to this specific link. """

        self.page = page
        """ The url of the page to which this entry points to. """

        self.definition = definition
        """ The definition of the term. """


class Glossary:
    """ The complete glossary for all sections """

    def __init__(self):
        self.clear()

    def add(self, section, term, linktype, page, definition=None):
        links = self._links(section, term, linktype)
        _id = f"{section}_{term}_{linktype}_{len(links)}".replace(" ", "_")
        links[_id] = Entry(_id, page, definition)
        return _id

    def has(self, section):
        """ Check if the glossary has a section named **section**.

            Args:
                section (str):
                    The name of the section to check

            Returns:
                bool:
                    True, if a section with the given name exists.
        """
        return section in self._glossary

    def get(self, section, term, linktype) -> list[Entry]:
        """ xGet a list of [Entry][mkdocs_ezglossary_plugin.glossary.Entry] instances
            for a specific **term** in a **section**.

            Args:
                section (str):
                    The name of the section
                term (str):
                    The term for which the [Entry] instances should be retreived.
                linktype (str):
                    Defines which type of links should be returned.

                    `refs`
                    : returns all references to the term

                    `defs`
                    : returns all definitions for the term

            Returns:
                A list of either `definitions` or `references` for the given term.
        """
        links = self._links(section, term, linktype).values()
        return list(links)

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
