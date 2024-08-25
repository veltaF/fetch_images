import unittest
import aiohttp
import logging
from unittest.mock import patch, AsyncMock, MagicMock

import modules.fetch_find as fetch_find


class TestFetchFind(unittest.IsolatedAsyncioTestCase):

    def test_find_images_from_html(self):
        html_content = '''
        <html>
            <body>
                <img src="/my/image1.jpg">
                <img src="image2.jpg">
                <div style="background-image:url('/my/background1.jpg');"></div>
                <div style="background:url('background2.jpg');"></div>
            </body>
        </html>
        '''
        base_url = 'http://test.com/'

        result = fetch_find.find_images_from_html(html_content, base_url)
        expected_result = [
            'http://test.com/my/image1.jpg',
            'http://test.com/image2.jpg',
            'http://test.com/my/background1.jpg',
            'http://test.com/background2.jpg'
        ]
        self.assertEqual(result, expected_result)

    def test_find_css_links(self):
        html_content = '<html><link rel="stylesheet" href="/my/style.css"><link rel="stylesheet" href="style2.css"></html>'
        base_url = 'http://test.com/'

        result = fetch_find.find_css_links(html_content, base_url)

        expected_result = ['http://test.com/my/style.css', 'http://test.com/style2.css']
        self.assertEqual(result, expected_result)

    async def test_find_images_from_css_files(self):
        css_urls = [
            'http://test.com/my/style.css',
            'http://test.com/style2.css'
        ]

        with patch('modules.fetch_find.fetch', new=AsyncMock()) as mock_fetch:
            mock_fetch.side_effect = [
                'body { background-image: url("/my/background1.jpg"); }',
                'body { background: url("background2.jpg"); }'
            ]

            result = await fetch_find.find_images_from_css_files(css_urls)
            expected_result = [
                'http://test.com/my/background1.jpg',
                'http://test.com/background2.jpg'
            ]
            self.assertEqual(result, expected_result)

    async def test_find_all_images_on_page(self):
        url = 'http://test.com/'

        mock_html_content = '<html><img src="/img1.jpg"><link rel="stylesheet" href="/style.css"></html>'
        with patch('modules.fetch_find.fetch', return_value=mock_html_content) as mock_fetch, \
                patch('modules.fetch_find.find_images_from_html', return_value=['http://test.com/img1.jpg']) as mock_find_images_from_html, \
                patch('modules.fetch_find.find_css_links', return_value=['http://test.com/style.css']) as mock_find_css_links, \
                patch('modules.fetch_find.find_images_from_css_files', return_value=['http://test.com/bg.jpg']) as mock_find_images_from_css_files:

            result = await fetch_find.find_all_images_on_page(url)

            mock_fetch.assert_called_once_with(url)
            mock_find_images_from_html.assert_called_once_with(mock_html_content, url)
            mock_find_css_links.assert_called_once_with(mock_html_content, url)
            mock_find_images_from_css_files.assert_called_once_with(['http://test.com/style.css'])

            expected_result = ['http://test.com/img1.jpg', 'http://test.com/bg.jpg']
            self.assertEqual(result, expected_result)

    async def test_find_all_images_on_page_fetch_error(self):
        logging.disable(logging.CRITICAL)
        url = 'http://test.com/'

        with patch('modules.fetch_find.fetch', side_effect=aiohttp.ClientError('Fetch error')):
            result = await fetch_find.find_all_images_on_page(url)
            self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
