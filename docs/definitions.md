# Definitions

term:term
:   A term is a definition of a word in your glossary.

    The same term can be defined in multiple <term:section|sections>

term:section
:   ezglossary supports adding terms to different sections. This
    allows defining multiple glossaries and printing individual
    <term:summary|summaries> for each section

term:summary
:   The summary is a list of all defined terms in a section.
    
    It contains links to their <term:definitions> and <term:references>.

term:definition
:   The definition of a term in a definition lists.

    The ezglossary plugin hooks in the html generation process,
    and looks for definition lists. In case it identifies
    a 

term:reference
:   The reference is a place in your documentation where you
    refer to a term by placing a [link](usage/linking.md).

## Summary

<glossary::term>
