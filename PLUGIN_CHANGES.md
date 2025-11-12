# Plugin Changes Documentation

## Overview

This document details the changes made to `plugin.py` to add section-specific `exclude_from_search` functionality to the mkdocs-ezglossary plugin. The changes enable users to exclude specific glossary sections from the search index while maintaining backward compatibility with the global boolean `exclude_from_search` configuration.

## Key Features Added

### 1. Section-Specific Search Exclusion
- Added per-section `exclude_from_search` configuration via `section_config`
- Enables fine-grained control over which glossary sections appear in search results
- Works by filtering search index content after build completion

### 2. Generic Implementation
- Uses dynamic glossary data structure access to work with any sections/terms
- No hardcoded section names - works with user-defined sections
- Regex-based pattern matching for robust content filtering

### 3. Print Site Compatibility
- Enhanced print-site plugin integration with anchor-only links for PDF output
- Improved tooltip rendering logic with sentence-based splitting
- UUID replacement during content processing for better print output

## Configuration Changes

### New Configuration Option
```python
exclude_from_search = config.config_options.Type(bool, default=False)
```

### Section-Specific Configuration Example
```yaml
plugins:
  - ezglossary:
      sections: [main, internal, roles, deprecated]
      section_config:
        - name: internal
          exclude_from_search: true
        - name: deprecated  
          exclude_from_search: true
```

## Implementation Details

### 1. Search Index Processing (`_clean_search_index`)

**Original Behavior:**
- Simple UUID cleanup from search index
- No content filtering capability

**Enhanced Behavior:**
- Maps glossary pages to their sections using `_get_glossary_pages_with_sections()`
- Checks both global and section-specific `exclude_from_search` settings
- Applies `_filter_excluded_sections_from_text()` to remove excluded content
- Maintains existing UUID cleanup functionality

**Key Code Addition:**
```python
# Check for section-specific exclusions
excluded_sections = []
for section in page_sections:
    if self._get_config(section, 'exclude_from_search'):
        excluded_sections.append(section)

if excluded_sections:
    # Filter out content from excluded sections
    filtered_text = self._filter_excluded_sections_from_text(original, excluded_sections)
```

### 2. Generic Content Filtering (`_filter_excluded_sections_from_text`)

**New Method - Core Innovation:**
- Dynamically identifies terms from excluded sections using glossary data structure
- Builds regex patterns to match terms and their definitions in search text
- Removes matching content while preserving other sections
- Handles both direct internal access and public API fallback

**Pattern Matching Strategy:**
```python
# Build pattern: "term definition_text"
# The search index format is: "term Has definition here.  next_term"
escaped_term = re.escape(term)
# Match term followed by content until period + spaces (more robust)
pattern = rf'\b{escaped_term}\b[^.]*?\.\s*'
```

### 3. Glossary Page Detection (`_get_glossary_pages_with_sections`)

**New Method:**
- Maps page URLs to the glossary sections they contain
- Normalizes URLs to .html format for consistency
- Supports both internal data access and public API fallback
- Enables targeted section filtering per page

### 4. Enhanced Link Processing

**Print Site Compatibility:**
- Modified `_replace_glossary_links()` to detect print-site plugin
- Uses anchor-only links (`#target`) instead of full URLs for PDF output
- Improved tooltip logic with sentence-based splitting for better readability

**UUID Processing Improvements:**
- Enhanced HTML entity decoding in link replacement
- Better error handling for malformed glossary references
- Cleaner regex patterns for UUID detection and removal

### 5. Build Process Integration (`on_post_build`)

**New Hook:**
- Processes print_page.html for print-site compatibility
- Cleans search index after build completion
- Ensures all glossary processing happens at the right time in MkDocs build pipeline

## Regex Patterns and Text Processing

### Search Index Content Structure
The search index stores content in format: `"term Has definition here. next_term Has other definition."`

### Exclusion Pattern Logic
```python
# Pattern matches:
# - Word boundary + escaped term + word boundary
# - Any characters (non-greedy) until period
# - Period + optional whitespace
pattern = rf'\b{escaped_term}\b[^.]*?\.\s*'
```

### Robustness Features
- Word boundary matching prevents partial word matches
- Non-greedy matching stops at first period to avoid over-matching
- Whitespace cleanup after pattern removal
- Error handling for invalid regex patterns

## Backward Compatibility

### Preserved Functionality
- All existing configuration options work unchanged
- Global `exclude_from_search: true` still excludes entire pages
- No breaking changes to existing plugin API
- Original tooltip and link processing behavior maintained

### Migration Path
- Existing configurations continue to work without modification
- New section-specific feature is opt-in via `section_config`
- Gradual migration possible - can mix global and section-specific settings

## Error Handling and Logging

### Comprehensive Logging
- Debug logs for pattern matching and exclusion results
- Info logs for successful filtering operations
- Warning logs for configuration errors or processing failures

### Graceful Degradation
- Fallback to public API if internal data access fails
- Continues processing if individual patterns fail
- Returns original content if filtering encounters errors

## Testing Implications

### Test Coverage Areas
1. **Configuration System**
   - Section-specific `exclude_from_search` parsing
   - Mixed global/section-specific configurations
   - Invalid section configurations

2. **Content Filtering**  
   - Regex pattern generation and matching
   - Multi-section exclusion scenarios
   - Edge cases (empty sections, duplicate terms)

3. **Search Index Processing**
   - UUID cleanup preservation
   - Content filtering accuracy
   - Page-to-section mapping

4. **Print Site Integration**
   - Anchor-only link generation
   - Print page processing
   - Tooltip rendering improvements

## Performance Considerations

### Efficiency Optimizations
- Direct internal data access preferred over public API iteration
- Compiled regex patterns for repeated matching
- Early exit conditions for empty exclusion lists
- Minimal memory footprint during filtering

### Scalability
- O(n) complexity for term pattern generation
- O(m) complexity for content filtering where m = content length
- Caching of page-to-section mappings
- Batch processing of exclusion patterns

## Summary

The enhanced plugin now provides:
- ✅ **Section-specific search exclusion** - Fine-grained control over search content
- ✅ **Generic implementation** - Works with any user-defined sections  
- ✅ **Backward compatibility** - No breaking changes to existing configurations
- ✅ **Robust processing** - Error handling and graceful degradation
- ✅ **Print site integration** - Enhanced PDF/print output compatibility
- ✅ **Comprehensive logging** - Detailed debugging and monitoring capabilities

The implementation successfully balances functionality, performance, and maintainability while providing a powerful new feature for mkdocs-ezglossary users.