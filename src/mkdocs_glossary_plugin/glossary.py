class Glossary:
    def __init__(self):
        self.clear()

    def add(self, section, term, linktype, page, desc=None):
        links = self._links(section, term, linktype)
        _id = f"{section}{term}{linktype}{len(links)}"
        links[_id] = (page, desc)
        return _id

    def has(self, section):
        return section in self._glossary

    def get(self, section, term, linktype):
        links = self._links(section, term, linktype)
        return links

    def terms(self, section):
        keys = list(self._section(section).keys())
        keys.sort()
        return keys

    def clear(self):
        self._glossary = {}

    def _links(self, section, term, linktype):
        return self._term(section, term)[linktype]

    def _term(self, section, term):
        if term not in self._section(section):
            self._section(section)[term] = {'defs': {}, 'refs': {}}
        return self._section(section)[term]

    def _section(self, section):
        if section not in self._glossary:
            self._glossary[section] = {}
        return self._glossary[section]
