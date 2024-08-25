import unittest
from modules.fetch_utils import is_valid_url, extract_urls

class TestFetchUtils(unittest.TestCase):

    def test_valid_url(self):
        self.assertTrue(is_valid_url('http://test.com'))
        self.assertTrue(is_valid_url('https://test.com'))

    def test_invalid_url(self):
        self.assertFalse(is_valid_url('test.com'))
        self.assertFalse(is_valid_url('ftp://test.com'))
        self.assertFalse(is_valid_url(''))

    def test_extract_urls(self):
        html_content = '''
        <html>
            <body>
                <img src="/images/pic1.jpg">
                <a href="http://example.com/page.html">Link</a>
                <img src="pic2.jpg">
                <div style="background-image:url('/images/bg.jpg');"></div>
            </body>
        </html>
        '''
        base_url = 'http://test.com/'
        img_pattern = r'<img [^>]*src="([^"]+)"'
        background_image_pattern = r'background(?:-image)?\s*:\s*url\(["\']?([^"\')]+)["\']?\)'

        img_urls = extract_urls(img_pattern, html_content, base_url)
        background_img_urls = extract_urls(background_image_pattern, html_content, base_url)
        all_urls = img_urls + background_img_urls

        expected_urls = [
            'http://test.com/images/pic1.jpg',
            'http://test.com/pic2.jpg',
            'http://test.com/images/bg.jpg'
        ]
        self.assertEqual(all_urls, expected_urls)


if __name__ == '__main__':
    unittest.main()
