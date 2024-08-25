#!/usr/bin/env python3
import sys
import os
import asyncio
import logging
from modules.fetch_utils import is_valid_url
from modules.fetch_find import find_all_images_on_page
from modules.fetch_download import download_images_concurrently


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)


async def main():
    if len(sys.argv) != 2:
        logging.error("Wrong number of arguments, usage: python fetch.py <your_argument>")
        sys.exit(1)

    url = sys.argv[1]
    if not is_valid_url(url):
        logging.error(f"Error: The argument '{url}' is not a valid URL.")
        sys.exit(1)
    logging.info(f"The URL you provided is: {url}")

    images_folder = 'downloaded_images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    img_urls = await find_all_images_on_page(url)
    if img_urls:
        logging.info(f"Found {len(img_urls)} images. Downloading...")
        await download_images_concurrently(img_urls, images_folder)
    else:
        logging.info("No images found or an error occurred.")


def sync_wrapper():
    asyncio.run(main())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[0] == __file__:
        asyncio.run(main())
    else:
        sync_wrapper()
