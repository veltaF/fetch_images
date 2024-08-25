import unittest
import asyncio
import aiohttp
from unittest import mock
from unittest.mock import patch, MagicMock
from modules.fetch_download import download_image_to_folder, download_images_concurrently

class TestDownloadImage(unittest.IsolatedAsyncioTestCase):

    async def test_download_image_to_folder(self):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.content.read = mock.AsyncMock(side_effect=[b'some data', b'more data', b''])

        mock_session = MagicMock()
        mock_session.get.return_value.__aenter__.return_value = mock_response

        image_url = "http://test.com/image.jpg"
        folder_path = "/folder"

        with patch("aiohttp.ClientSession") as mock_ClientSession, \
                patch("builtins.open", new_callable=mock.mock_open) as mock_open, \
                patch("os.makedirs") as mock_makedirs:

            mock_ClientSession.return_value.__aenter__.return_value = mock_session

            await download_image_to_folder(image_url, folder_path)

            mock_makedirs.assert_called_once()
            mock_open.assert_called_once()
            mock_open().write.assert_called()

    async def test_download_images_concurrently(self):
        image_urls = [
            "http://test.com/image1.jpg",
            "http://test.com/image2.jpg",
            "http://test.com/image3.jpg"
        ]
        folder_path = "/folder"

        with patch('modules.fetch_download.download_image_to_folder') as mock_download_image_to_folder:
            mock_download_image_to_folder.return_value = asyncio.Future()
            mock_download_image_to_folder.return_value.set_result(None)

            await download_images_concurrently(image_urls, folder_path)

            self.assertEqual(mock_download_image_to_folder.call_count, len(image_urls))
            for url in image_urls:
                mock_download_image_to_folder.assert_any_call(url, folder_path)

    async def test_download_image_to_folder_file_write_error(self):
        image_url = 'http://test.com/image.jpg'
        folder_path = './test_folder'

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.content.read = MagicMock(return_value=b'image data')

        mock_session = MagicMock()
        mock_session.get.return_value.__aenter__.return_value = mock_response

        with patch("aiohttp.ClientSession") as mock_ClientSession, \
                patch("builtins.open", new_callable=mock.mock_open) as mock_file, \
                patch("os.makedirs") as mock_makedirs:

            mock_ClientSession.return_value.__aenter__.return_value = mock_session
            mock_file.side_effect = IOError("File write error")
            with self.assertRaises(IOError):
                await download_image_to_folder(image_url, folder_path)


if __name__ == '__main__':
    unittest.main()
    