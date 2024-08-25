from urllib.parse import urlparse
import os
import aiohttp
import asyncio
import logging

async def download_image_to_folder(image_url, folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                response.raise_for_status()

                image_name_extracted = os.path.basename(urlparse(image_url).path)
                image_path = os.path.join(folder_path, image_name_extracted)

                with open(image_path, 'wb') as file:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        file.write(chunk)

        logging.info(f"Downloaded: {image_url} to {folder_path}")
    except aiohttp.ClientError as e:
        logging.error(f"Error downloading image {image_url}: {e}")


async def download_images_concurrently(image_urls, folder_path):
    tasks = [download_image_to_folder(url, folder_path) for url in image_urls]
    await asyncio.gather(*tasks)
 