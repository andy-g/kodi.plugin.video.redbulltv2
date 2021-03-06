#!/usr/bin/env python
import sys, os
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import lib.redbulltv_client as redbulltv

class ITTestRedbulltvClient(unittest.TestCase):
    redbulltv_client = redbulltv.RedbullTVClient('4')

    def test_get_root_menu(self):
        test_data = [
            (
                None,
                [
                    {'url': 'https://appletv.redbull.tv/products/discover', 'is_content': False, 'title': 'Discover'},
                    {'url': 'https://appletv.redbull.tv/products/tv', 'is_content': False, 'title': 'TV'},
                    {'url': 'https://appletv.redbull.tv/products/channels', 'is_content': False, 'title': 'Channels'},
                    {'url': 'https://appletv.redbull.tv/products/calendar', 'is_content': False, 'title': 'Calendar'},
                    {'url': 'https://appletv.redbull.tv/search?q=', 'is_content': False, 'title': 'Search'}
                ]
            ),
        ]
        for inp, expected in test_data:
            self.assertEqual(self.redbulltv_client.get_items(inp), expected)

    def test_get_discover_categories(self):
        """
        List the categorires from the Discover Page
        Check for more than 5 categories and explicitly check the first 2
        """
        test_data = ('https://appletv.redbull.tv/products/discover', None)

        result = self.redbulltv_client.get_items(*test_data)
        self.assertGreater(len(result), 5)
        self.assertEqual(result[0].get("category"), "Featured")

    def test_get_category_items(self):
        """
        List the items for a specific category on the Discover Page
        Check for more than 5 items in the 'Featured' & 'Daily Highlights' categories
        """
        test_data = [
            ('https://appletv.redbull.tv/products/discover', 'Featured'),
            ('https://appletv.redbull.tv/products/discover', 'Daily Highlights'),
        ]

        for inp in test_data:
            result = self.redbulltv_client.get_items(*inp)
            self.assertGreater(len(result), 5)

    def test_watch_now_stream(self):
        """
        Test the Watch Now Live Stream and confirm a resolution specific playlist is returned
        """
        test_data = (
            ('https://appletv.redbull.tv/linear_stream', None),
            [
                ('Lean back and experience the best of Red Bull TV', True, 'Watch Now'),
                'https://dms.redbull.tv/v3/linear-borb/_v3/playlist.m3u8'
            ]
        )
        inp, expected = test_data
        result = self.redbulltv_client.get_items(*inp)
        self.assertEqual(
            (result[0].get("summary"), result[0].get("is_stream"), result[0].get("title")),
            expected[0]
        )
        self.assertNotEqual(result[0].get('url'), expected[1])

    def test_search(self):
        """
        Test the Search functionality
        """
        test_data = ('https://appletv.redbull.tv/search?q=follow', None)
        result = self.redbulltv_client.get_items(*test_data)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
