# SPDX-License-Identifier: AGPL-3.0-or-later
# pylint: disable=missing-module-docstring

from unittest import mock
import sys
import os

# Add engines directory to path for direct import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'searx', 'engines'))

from tests import SearxTestCase


class TestZbmathEngine(SearxTestCase):
    """Tests for zbMATH Open engine"""

    def setUp(self):
        # Import directly without loading full searx.engines
        import zbmath
        self.zbmath = zbmath

    def test_request(self):
        """Test request function builds correct URL"""
        query = 'topology'
        params = {'pageno': 1}
        result = self.zbmath.request(query, params)
        
        self.assertIn('url', result)
        self.assertIn('api.zbmath.org', result['url'])
        self.assertIn('search_string=topology', result['url'])
        self.assertIn('results_per_page=10', result['url'])
        self.assertIn('page=0', result['url'])

    def test_request_paging(self):
        """Test request function handles pagination"""
        query = 'algebra'
        params = {'pageno': 3}
        result = self.zbmath.request(query, params)
        
        self.assertIn('page=2', result['url'])

    def test_response_empty(self):
        """Test response handles empty results"""
        response = mock.Mock(text='{"result": []}', status_code=200)
        results = self.zbmath.response(response)
        
        self.assertEqual(results, [])

    def test_response_missing_result(self):
        """Test response handles missing result key"""
        response = mock.Mock(text='{}', status_code=200)
        results = self.zbmath.response(response)
        
        self.assertEqual(results, [])

    def test_response_basic(self):
        """Test response parses basic result"""
        json_response = '''
        {
            "result": [
                {
                    "title": {"title": "Test Title"},
                    "contributors": {"authors": [{"name": "Smith, John"}]},
                    "year": "2020",
                    "source": {"source": "Journal of Math"},
                    "zbmath_url": "https://zbmath.org/1234567"
                }
            ]
        }
        '''
        response = mock.Mock(text=json_response, status_code=200)
        results = self.zbmath.response(response)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Test Title')
        self.assertEqual(results[0]['url'], 'https://zbmath.org/1234567')
        self.assertIn('Smith, John', results[0]['content'])
        self.assertIn('2020', results[0]['content'])
        self.assertIn('Journal of Math', results[0]['content'])

    def test_response_multiple_authors(self):
        """Test response handles multiple authors"""
        json_response = '''
        {
            "result": [
                {
                    "title": {"title": "Multi-Author Paper"},
                    "contributors": {
                        "authors": [
                            {"name": "Smith, John"},
                            {"name": "Jones, Jane"},
                            {"name": "Brown, Bob"},
                            {"name": "White, Alice"}
                        ]
                    },
                    "year": "2019",
                    "source": {"source": "Math Review"},
                    "zbmath_url": "https://zbmath.org/7654321"
                }
            ]
        }
        '''
        response = mock.Mock(text=json_response, status_code=200)
        results = self.zbmath.response(response)
        
        self.assertEqual(len(results), 1)
        self.assertIn('et al.', results[0]['content'])

    def test_response_subtitle(self):
        """Test response handles subtitle"""
        json_response = '''
        {
            "result": [
                {
                    "title": {"title": "Main Title", "subtitle": "A Subtitle"},
                    "contributors": {"authors": [{"name": "Author, A."}]},
                    "year": "2021",
                    "source": {"source": ""},
                    "zbmath_url": "https://zbmath.org/1111111"
                }
            ]
        }
        '''
        response = mock.Mock(text=json_response, status_code=200)
        results = self.zbmath.response(response)
        
        self.assertEqual(results[0]['title'], 'Main Title: A Subtitle')
