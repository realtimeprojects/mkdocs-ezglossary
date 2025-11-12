"""
Tests for section-specific exclude_from_search functionality in mkdocs-ezglossary plugin.

These tests cover the new functionality that allows excluding specific glossary sections
from the search index while maintaining backward compatibility with global exclusion.
"""

import json
import os
import tempfile
import pytest
from unittest.mock import Mock, patch

from mkdocs_ezglossary_plugin.plugin import GlossaryPlugin


class TestSectionSpecificExcludeFromSearch:
    """Test section-specific exclude_from_search functionality."""

    def setup_method(self):
        """Set up test environment for each test."""
        self.plugin = GlossaryPlugin()
        
        # Create proper config object with attributes
        config_mock = Mock()
        config_mock.sections = ['main', 'internal', 'roles', 'deprecated']  
        config_mock.exclude_from_search = False
        config_mock.section_config = [
            {'name': 'internal', 'exclude_from_search': True},
            {'name': 'deprecated', 'exclude_from_search': True}
        ]
        self.plugin.config = config_mock
        
        # Set up UUIDs for testing (these are set in __init__ normally)
        self.plugin._uuid = "6251a85a-47d0-11ee-be56-0242ac120002"  
        self.plugin._reflink = "886d7696-137e-4a59-a39d-6f7d311d5bd1"
        
        # Mock the _get_config method
        self.plugin._get_config = Mock(side_effect=self._mock_get_config)
        
    def _mock_get_config(self, section, option):
        """Mock _get_config method to return section-specific configurations."""
        if option == 'exclude_from_search':
            for config in getattr(self.plugin.config, 'section_config', []):
                if config.get('name') == section:
                    return config.get('exclude_from_search', False)
            return getattr(self.plugin.config, 'exclude_from_search', False)
        return False

    def test_get_glossary_pages_with_sections(self):
        """Test _get_glossary_pages_with_sections method."""
        # Mock glossary with sections and pages
        mock_entry1 = Mock()
        mock_entry1.page.url = 'glossary.md'
        mock_entry2 = Mock()
        mock_entry2.page.url = 'admin/'
        mock_entry3 = Mock()
        mock_entry3.page.url = 'roles.html'
        
        self.plugin._glossary = Mock()
        self.plugin._glossary._sections = {
            'main': {'term1': {'defs': [mock_entry1]}},
            'internal': {'term2': {'defs': [mock_entry2]}}, 
            'roles': {'term3': {'defs': [mock_entry3]}}
        }
        
        result = self.plugin._get_glossary_pages_with_sections()
        
        expected = {
            'glossary.html': {'main'},
            'admin.html': {'internal'},
            'roles.html': {'roles'}
        }
        
        assert result == expected

    def test_get_glossary_pages_with_sections_fallback(self):
        """Test _get_glossary_pages_with_sections with public API fallback."""
        # Mock glossary without _sections attribute
        self.plugin._glossary = Mock()
        del self.plugin._glossary._sections  # Remove _sections to trigger fallback
        
        # Configure public API methods
        self.plugin._glossary.has.return_value = True
        self.plugin._glossary.terms.return_value = ['term1', 'term2']
        
        mock_entry = Mock()
        mock_entry.page.url = 'test-page.md'
        self.plugin._glossary.get.return_value = [mock_entry]
        
        result = self.plugin._get_glossary_pages_with_sections()
        
        # Should have called public API methods
        assert self.plugin._glossary.has.called
        assert 'test-page.html' in result

    def test_filter_excluded_sections_from_text_basic(self):
        """Test basic text filtering for excluded sections."""
        # Mock glossary with terms from different sections
        mock_entry1 = Mock()
        mock_entry1.term = "admin"
        mock_entry2 = Mock()
        mock_entry2.term = "deprecated_feature"
        
        self.plugin._glossary = Mock()
        self.plugin._glossary._sections = {
            'internal': {'admin': {'defs': [mock_entry1]}},
            'deprecated': {'deprecated_feature': {'defs': [mock_entry2]}}
        }
        
        # Test text with terms from both excluded sections
        test_text = """
        admin Has administrative privileges. 
        user Can access basic features.
        deprecated_feature Was removed in version 2.0.
        manager Has elevated permissions.
        """
        
        result = self.plugin._filter_excluded_sections_from_text(
            test_text, ['internal', 'deprecated']
        )
        
        # Should remove 'admin' and 'deprecated_feature' entries
        assert 'admin Has administrative privileges.' not in result
        assert 'deprecated_feature Was removed in version 2.0.' not in result
        # Should preserve other content
        assert 'user Can access basic features.' in result
        assert 'manager Has elevated permissions.' in result

    def test_filter_excluded_sections_from_text_empty_exclusions(self):
        """Test text filtering with empty exclusions list."""
        test_text = "Some test content here."
        
        result = self.plugin._filter_excluded_sections_from_text(test_text, [])
        
        # Should return original text unchanged
        assert result == test_text

    def test_filter_excluded_sections_from_text_no_matches(self):
        """Test text filtering when no terms match."""
        self.plugin._glossary = Mock()
        self.plugin._glossary._sections = {
            'internal': {'nonexistent': {'defs': []}}
        }
        
        test_text = "This text has no matching terms."
        
        result = self.plugin._filter_excluded_sections_from_text(
            test_text, ['internal']
        )
        
        # Should return original text (minus extra whitespace cleanup)
        assert result.strip() == test_text.strip()

    def test_filter_excluded_sections_fallback_api(self):
        """Test text filtering with public API fallback."""
        # Mock glossary without _sections
        self.plugin._glossary = Mock()
        del self.plugin._glossary._sections
        
        # Configure public API
        self.plugin._glossary.has.return_value = True
        self.plugin._glossary.terms.return_value = ['test_term']
        
        mock_entry = Mock()
        mock_entry.term = "test_term"
        self.plugin._glossary.get.return_value = [mock_entry]
        
        test_text = "test_term Has some definition here."
        
        result = self.plugin._filter_excluded_sections_from_text(
            test_text, ['test_section']
        )
        
        # Should have attempted to use public API
        assert self.plugin._glossary.has.called
        assert self.plugin._glossary.terms.called

    def test_clean_search_index_global_exclude(self):
        """Test search index cleaning with global exclude_from_search."""
        self.plugin.config.exclude_from_search = True
        
        # Create temporary search index
        with tempfile.TemporaryDirectory() as temp_dir:
            search_dir = os.path.join(temp_dir, 'search')
            os.makedirs(search_dir)
            
            search_index_path = os.path.join(search_dir, 'search_index.json')
            search_data = {
                'docs': [
                    {
                        'title': 'Test Page',
                        'text': 'admin Has administrative privileges. user Can login.',
                        'location': 'glossary.html'
                    }
                ]
            }
            
            with open(search_index_path, 'w') as f:
                json.dump(search_data, f)
            
            # Mock page-to-sections mapping
            self.plugin._get_glossary_pages_with_sections = Mock(return_value={
                'glossary.html': {'main', 'internal'}
            })
            
            self.plugin._clean_search_index(temp_dir)
            
            # Check that content was removed due to global exclusion
            with open(search_index_path, 'r') as f:
                result_data = json.load(f)
            
            assert result_data['docs'][0]['text'] == ''

    def test_clean_search_index_section_specific_exclude(self):
        """Test search index cleaning with section-specific exclusions."""
        # Create temporary search index
        with tempfile.TemporaryDirectory() as temp_dir:
            search_dir = os.path.join(temp_dir, 'search')
            os.makedirs(search_dir)
            
            search_index_path = os.path.join(search_dir, 'search_index.json')
            search_data = {
                'docs': [
                    {
                        'title': 'Test Page',
                        'text': 'admin Has admin privileges. user Can login. deprecated_feature Was removed.',
                        'location': 'glossary.html'
                    }
                ]
            }
            
            with open(search_index_path, 'w') as f:
                json.dump(search_data, f)
            
            # Mock page-to-sections mapping
            self.plugin._get_glossary_pages_with_sections = Mock(return_value={
                'glossary.html': {'main', 'internal', 'deprecated'}
            })
            
            # Mock text filtering
            expected_filtered = 'user Can login.'
            self.plugin._filter_excluded_sections_from_text = Mock(return_value=expected_filtered)
            
            self.plugin._clean_search_index(temp_dir)
            
            # Verify filtering was called with correct excluded sections
            self.plugin._filter_excluded_sections_from_text.assert_called_once()
            args = self.plugin._filter_excluded_sections_from_text.call_args
            assert 'internal' in args[0][1]  # excluded_sections parameter
            assert 'deprecated' in args[0][1]
            
            # Check that filtered content was saved
            with open(search_index_path, 'r') as f:
                result_data = json.load(f)
            
            assert result_data['docs'][0]['text'] == expected_filtered

    def test_clean_search_index_no_exclusions(self):
        """Test search index cleaning with no exclusions configured."""
        self.plugin.config.exclude_from_search = False
        self.plugin.config.section_config = []  # No section-specific exclusions
        
        # Create temporary search index
        with tempfile.TemporaryDirectory() as temp_dir:
            search_dir = os.path.join(temp_dir, 'search')
            os.makedirs(search_dir)
            
            search_index_path = os.path.join(search_dir, 'search_index.json')
            original_text = 'admin Has privileges. user Can login.'
            # Use more realistic UUID pattern that matches the actual regex patterns used
            uuid_pattern = f'{self.plugin._uuid}:12345678901234567890123456789012:<link text>'
            reflink_pattern = f'{self.plugin._reflink}:section:term'
            search_data = {
                'docs': [
                    {
                        'title': f'Test {uuid_pattern} Title',
                        'text': f'{original_text} {reflink_pattern} more text',
                        'location': 'test.html'
                    }
                ]
            }
            
            with open(search_index_path, 'w') as f:
                json.dump(search_data, f)
            
            # Mock empty page-to-sections mapping
            self.plugin._get_glossary_pages_with_sections = Mock(return_value={})
            
            self.plugin._clean_search_index(temp_dir)
            
            # Check that only UUIDs were cleaned, content preserved
            with open(search_index_path, 'r') as f:
                result_data = json.load(f)
            
            # UUIDs should be removed from title and text
            assert self.plugin._uuid not in result_data['docs'][0]['title']
            assert self.plugin._reflink not in result_data['docs'][0]['text']
            
            # But original content should be preserved
            assert 'Test' in result_data['docs'][0]['title']
            assert 'Title' in result_data['docs'][0]['title']
            assert original_text in result_data['docs'][0]['text']
            assert 'more text' in result_data['docs'][0]['text']

    def test_clean_search_index_missing_file(self):
        """Test search index cleaning when search_index.json doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Don't create search directory/file
            
            # Should not raise exception
            self.plugin._clean_search_index(temp_dir)

    def test_clean_search_index_invalid_json(self):
        """Test search index cleaning with invalid JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            search_dir = os.path.join(temp_dir, 'search')
            os.makedirs(search_dir)
            
            search_index_path = os.path.join(search_dir, 'search_index.json')
            
            # Write invalid JSON
            with open(search_index_path, 'w') as f:
                f.write('{ invalid json }')
            
            # Should not raise exception, should log warning
            with patch('mkdocs_ezglossary_plugin.plugin.log') as mock_log:
                self.plugin._clean_search_index(temp_dir)
                mock_log.warning.assert_called()

    def test_url_normalization_patterns(self):
        """Test URL normalization in _get_glossary_pages_with_sections."""
        mock_entries = []
        urls = ['page.md', 'directory/', 'file.html', 'noextension']
        expected_normalized = ['page.html', 'directory.html', 'file.html', 'noextension.html']
        
        for url in urls:
            mock_entry = Mock()
            mock_entry.page.url = url
            mock_entries.append(mock_entry)
        
        self.plugin._glossary = Mock()
        self.plugin._glossary._sections = {
            'test': {f'term{i}': {'defs': [entry]} for i, entry in enumerate(mock_entries)}
        }
        
        result = self.plugin._get_glossary_pages_with_sections()
        
        for expected_url in expected_normalized:
            assert expected_url in result
            assert 'test' in result[expected_url]

    def test_regex_pattern_generation(self):
        """Test regex pattern generation for term exclusion."""
        # Mock glossary with realistic terms (avoiding complex special chars that break word boundaries)
        special_terms = ["admin_user", "role_admin", "test_deprecated"]
        mock_entries = []
        
        for term in special_terms:
            mock_entry = Mock()
            mock_entry.term = term
            mock_entries.append(mock_entry)
        
        self.plugin._glossary = Mock()
        self.plugin._glossary._sections = {
            'test': {
                term: {'defs': [entry]} 
                for term, entry in zip(special_terms, mock_entries)
            }
        }
        
        test_text = """
        admin_user Has special access.
        role_admin Is a system role.
        test_deprecated Should be excluded.
        normal_term Stays in results.
        """
        
        result = self.plugin._filter_excluded_sections_from_text(test_text, ['test'])
        
        # All test section terms should be excluded
        for term in special_terms:
            assert term not in result
        
        # Normal term should remain
        assert 'normal_term Stays in results.' in result

    def test_mixed_global_and_section_exclusions(self):
        """Test configuration with both global and section-specific exclusions."""
        # Test that section-specific takes precedence when global is False
        self.plugin.config.exclude_from_search = False
        
        with tempfile.TemporaryDirectory() as temp_dir:
            search_dir = os.path.join(temp_dir, 'search')
            os.makedirs(search_dir)
            
            search_index_path = os.path.join(search_dir, 'search_index.json')
            search_data = {
                'docs': [
                    {
                        'title': 'Mixed Test',
                        'text': 'content from various sections',
                        'location': 'glossary.html'
                    }
                ]
            }
            
            with open(search_index_path, 'w') as f:
                json.dump(search_data, f)
            
            # Mock page with multiple sections, some excluded
            self.plugin._get_glossary_pages_with_sections = Mock(return_value={
                'glossary.html': {'main', 'internal', 'roles'}
            })
            
            # Mock filtering
            self.plugin._filter_excluded_sections_from_text = Mock(return_value='filtered content')
            
            self.plugin._clean_search_index(temp_dir)
            
            # Should have called filtering with only the excluded sections
            self.plugin._filter_excluded_sections_from_text.assert_called_once()
            args = self.plugin._filter_excluded_sections_from_text.call_args[0]
            excluded_sections = args[1]
            
            # Should only include sections configured for exclusion
            assert 'internal' in excluded_sections
            assert 'main' not in excluded_sections  # main has no exclude config

    @pytest.mark.parametrize("sections,expected_excluded", [
        (['internal'], ['internal']),
        (['internal', 'deprecated'], ['internal', 'deprecated']),
        (['main'], []),  # main has no exclude_from_search config
        ([], []),
        (['nonexistent'], []),
    ])
    def test_section_exclusion_logic(self, sections, expected_excluded):
        """Test section exclusion logic with various section combinations."""
        # Mock page with specified sections
        self.plugin._get_glossary_pages_with_sections = Mock(return_value={
            'test.html': set(sections)
        })
        
        # Mock filtering to capture what sections are excluded
        captured_exclusions = []
        def capture_exclusions(text, excluded_sections):
            captured_exclusions.extend(excluded_sections)
            return text
        
        self.plugin._filter_excluded_sections_from_text = Mock(side_effect=capture_exclusions)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            search_dir = os.path.join(temp_dir, 'search')
            os.makedirs(search_dir)
            
            search_index_path = os.path.join(search_dir, 'search_index.json')
            search_data = {
                'docs': [{'title': 'Test', 'text': 'test content', 'location': 'test.html'}]
            }
            
            with open(search_index_path, 'w') as f:
                json.dump(search_data, f)
            
            self.plugin._clean_search_index(temp_dir)
            
            # Check that correct sections were excluded
            assert set(captured_exclusions) == set(expected_excluded)


class TestSearchIndexIntegration:
    """Integration tests for search index processing."""
    
    def setup_method(self):
        """Set up integration test environment."""  
        self.plugin = GlossaryPlugin()
        
        # Create proper config object with attributes
        config_mock = Mock()
        config_mock.sections = ['main', 'internal']
        config_mock.exclude_from_search = False
        config_mock.section_config = [{'name': 'internal', 'exclude_from_search': True}]
        self.plugin.config = config_mock
        
        # Set up UUIDs for testing
        self.plugin._uuid = "6251a85a-47d0-11ee-be56-0242ac120002"
        self.plugin._reflink = "886d7696-137e-4a59-a39d-6f7d311d5bd1"
        
        self.plugin._get_config = Mock(side_effect=self._mock_get_config)

    def _mock_get_config(self, section, option):
        """Mock configuration lookup."""
        if option == 'exclude_from_search' and section == 'internal':
            return True
        return False

    def test_end_to_end_search_filtering(self):
        """Test complete search index filtering workflow."""
        # Create realistic glossary structure
        admin_entry = Mock()
        admin_entry.term = "admin"
        admin_entry.page.url = "glossary.html"
        
        user_entry = Mock()
        user_entry.term = "user" 
        user_entry.page.url = "glossary.html"
        
        self.plugin._glossary = Mock()
        self.plugin._glossary._sections = {
            'internal': {'admin': {'defs': [admin_entry]}},
            'main': {'user': {'defs': [user_entry]}}
        }
        
        # Create search index with mixed content
        with tempfile.TemporaryDirectory() as temp_dir:
            search_dir = os.path.join(temp_dir, 'search')
            os.makedirs(search_dir)
            
            search_index_path = os.path.join(search_dir, 'search_index.json')
            search_data = {
                'docs': [
                    {
                        'title': 'Glossary Page',
                        'text': 'admin Has administrative access. user Can log into system. manager Oversees operations.',
                        'location': 'glossary.html'
                    },
                    {
                        'title': 'Other Page', 
                        'text': 'No glossary terms here.',
                        'location': 'other.html'
                    }
                ]
            }
            
            with open(search_index_path, 'w') as f:
                json.dump(search_data, f)
            
            # Run the search index cleaning
            self.plugin._clean_search_index(temp_dir)
            
            # Verify results
            with open(search_index_path, 'r') as f:
                result_data = json.load(f)
            
            glossary_doc = result_data['docs'][0]
            other_doc = result_data['docs'][1]
            
            # Glossary page should have 'admin' removed but 'user' preserved
            assert 'admin Has administrative access.' not in glossary_doc['text']
            assert 'user Can log into system.' in glossary_doc['text']
            assert 'manager Oversees operations.' in glossary_doc['text']
            
            # Other page should be unchanged
            assert other_doc['text'] == 'No glossary terms here.'

    def test_multiple_pages_different_sections(self):
        """Test filtering across multiple pages with different section compositions."""
        # Create glossary with terms across different pages
        entries = {
            'admin': Mock(term="admin", page=Mock(url="admin.html")),
            'user': Mock(term="user", page=Mock(url="users.html")), 
            'role': Mock(term="role", page=Mock(url="admin.html")),
        }
        
        self.plugin._glossary = Mock()
        self.plugin._glossary._sections = {
            'internal': {
                'admin': {'defs': [entries['admin']]},
                'role': {'defs': [entries['role']]}
            },
            'main': {'user': {'defs': [entries['user']]}}
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            search_dir = os.path.join(temp_dir, 'search')
            os.makedirs(search_dir)
            
            search_index_path = os.path.join(search_dir, 'search_index.json')
            search_data = {
                'docs': [
                    {
                        'title': 'Admin Page',
                        'text': 'admin Manages system. role Defines permissions.',
                        'location': 'admin.html'
                    },
                    {
                        'title': 'Users Page',
                        'text': 'user Accesses features.',
                        'location': 'users.html'
                    }
                ]
            }
            
            with open(search_index_path, 'w') as f:
                json.dump(search_data, f)
            
            self.plugin._clean_search_index(temp_dir)
            
            with open(search_index_path, 'r') as f:
                result_data = json.load(f)
            
            admin_doc = next(d for d in result_data['docs'] if d['location'] == 'admin.html')
            users_doc = next(d for d in result_data['docs'] if d['location'] == 'users.html')
            
            # Admin page should have internal terms removed
            assert 'admin Manages system.' not in admin_doc['text']
            assert 'role Defines permissions.' not in admin_doc['text']
            
            # Users page should be unchanged (no internal terms)
            assert 'user Accesses features.' in users_doc['text']