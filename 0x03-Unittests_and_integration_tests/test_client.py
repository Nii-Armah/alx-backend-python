#!/usr/bin/env python3
"""
Tests for client module.

TestGithubOrgClient:
    Tests for client.GithubOrgClient.
"""

import unittest
from unittest.mock import patch

from client import GithubOrgClient

from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Tests for client.GithubOrgClient."""
    @parameterized.expand([
        ('google', ),
        ('abc', )
    ])
    @patch('client.get_json')
    def test_org(self, org, get_json_mock, ) -> None:
        return_value = {'login': 'interns'}
        get_json_mock.return_value = return_value


        client = GithubOrgClient(org)
        self.assertEqual(client.org, return_value)
        get_json_mock.assert_called_once_with(GithubOrgClient.ORG_URL.format(org=org))

