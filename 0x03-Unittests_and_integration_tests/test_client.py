#!/usr/bin/env python3
"""
Tests for client module.

TestGithubOrgClient:
    Tests for client.GithubOrgClient.

TestIntegrationGithubOrgClient:
    Integration tests for client.GithubOrgClient.
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

from parameterized import parameterized, parameterized_class


class TestGithubOrgClient(unittest.TestCase):
    """Tests for client.GithubOrgClient."""
    @parameterized.expand([
        ('google', ),
        ('abc', )
    ])
    @patch('client.get_json')
    def test_org(self, org, get_json_mock, ) -> None:
        """
        Validate return value of org attribute of a GithubOrgClient instance.
        """

        return_value = {'login': 'interns'}
        get_json_mock.return_value = return_value

        client = GithubOrgClient(org)
        self.assertEqual(client.org, return_value)
        get_json_mock.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org)
        )

    def test_public_repos_url(self) -> None:
        """
        Validate return value of _public_repos_url of a GithubOrgClient
        instance.
        """

        client = GithubOrgClient('google')

        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                'repos_url': 'https://api.github.com/orgs/google/repos'
            }

            self.assertEqual(
                client._public_repos_url,
                'https://api.github.com/orgs/google/repos'
            )

    @patch('client.get_json')
    def test_public_repos(self, get_json_mock) -> None:
        """
        Validate return value of public_repos attribute of a GithubOrgClient.
        """

        get_json_mock.return_value = [
            {'name': 'google-test'},
            {'name': 'chrome'},
            {'name': 'android'}
        ]

        with patch.object(
                GithubOrgClient,
                '_public_repos_url',
                new_callable=PropertyMock
        ) as public_repos_url_mock:
            public_repos_url_mock.return_value = 'https://api.github.com/repos'
            client = GithubOrgClient('google')

            self.assertEqual(
                client.public_repos(),
                ['google-test', 'chrome', 'android']
            )
            get_json_mock.assert_called_once()
            public_repos_url_mock.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False)
    ])
    def test_has_license(self, license_obj, license_key, result) -> None:
        """
        Validate return value of has_licence attribute of a GithubOrgClient
        instance.
        """

        client = GithubOrgClient('google')
        self.assertEqual(
            client.has_license(license_obj, license_key=license_key),
            result
        )


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for client.GithubOrgClient."""
    @classmethod
    def setUpClass(cls) -> None:
        cls.get_patcher = patch('requests.get')
        cls.get_mock = cls.get_patcher.start()

        def get_mock(url: str):
            mock_resp = Mock()
            if url.endswith('/orgs/google'):
                mock_resp.json.return_value = cls.org_payload
            elif url.endswith('/orgs/google/repos'):
                mock_resp.json.return_value = cls.repos_payload

            return mock_resp

        cls.get_mock.side_effect = get_mock

    @classmethod
    def tearDownClass(cls) -> None:
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Validate public_repos method of client.GithubOrgClient against fixtures
        provisioned within fixtures.py when no license is provided.
        """

        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Validate public_repos method of client.GithubOrgClient against fixtures
        provisioned within fixtures.py when a specific license is provided.
        """
        client = GithubOrgClient('google')
        self.assertEqual(
            client.public_repos(license='apache-2.0'),
            self.apache2_repos
        )
