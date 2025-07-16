#!/usr/bin/env python3
"""
Tests for utilities module.

TestAccessNestedMap:
    Tests for utils.access_nested_map.

TestGetJson:
    Tests for utils.get_json.

TestMemoize:
    Tests for utils.memoize.
"""

import unittest
from unittest.mock import Mock, patch

from utils import access_nested_map, get_json, memoize

from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Tests for utils.access_nested_map."""
    @parameterized.expand([
        ({'a': 1}, ('a',), 1),
        ({'a': {'b': 2}}, ('a',), {'b': 2}),
        ({'a': {'b': 2}}, ('a', 'b'), 2),
    ])
    def test_access_nested_map(self, nested_map, path, output) -> None:
        """
        utils.access_nested_map returns a valid output for a given nested map
        and path input pair.
        """
        self.assertEqual(access_nested_map(nested_map, path), output)

    @parameterized.expand([
        ({}, ('a', )),
        ({'a': 1}, ('a', 'b'))
    ])
    def test_access_nested_map_exception(self, nested_map, path) -> None:
        """
        utils.access_nested_map raises an exception when for a given nested
        map, there is no key-sequence corresponding to path specified in
        the path input variable.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for utils.get_json."""
    @parameterized.expand([
        ('http://example.com', {"payload": True}),
        ('http://holberton.io', {"payload": False})
    ])
    @patch('utils.requests')
    def test_get_json(self, url, payload, mock_requests) -> None:
        """
        utils.get_json returns a valid json response corresponding to a valid
        format for any given valid input.
        """
        mock_response = Mock()
        mock_response.json.return_value = payload
        mock_requests.get.return_value = mock_response

        response = get_json(url)
        mock_requests.get.assert_called_once_with(url)
        self.assertEqual(response, payload)


class TestMemoize(unittest.TestCase):
    """Tests for utils.memoize."""
    def test_memoize(self) -> None:
        """
        utils.memoize caches the return value of a_property to avoid
        unnecessary calls to a_method.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_class = TestClass()

        with patch.object(
                TestClass,
                'a_method',
                return_value=42
        ) as mock_method:
            self.assertEqual(test_class.a_property, 42)
            self.assertEqual(test_class.a_property, 42)
            mock_method.assert_called_once()
