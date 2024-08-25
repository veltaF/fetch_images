import logging
import aiohttp
from modules.fetch_utils import extract_urls, fetch

IMG_TAG_PATTERN = r'<img [^>]*src="([^"]+)"'
BACKGROUND_IMAGE_PATTERN = r'background(?:-image)?\s*:\s*url\(["\']?([^"\')]+)["\']?\)'
CSS_LINK_PATTERN = r'<link [^>]*rel="stylesheet"[^>]*href="([^"]+)"'


def find_images_from_html(html_content, base_url):
    img_urls = extract_urls(IMG_TAG_PATTERN, html_content, base_url)
    background_img_urls = extract_urls(BACKGROUND_IMAGE_PATTERN, html_content, base_url)
    return img_urls + background_img_urls


def find_css_links(html_content, base_url):
    return extract_urls(CSS_LINK_PATTERN, html_content, base_url)


async def find_images_from_css_files(css_urls):
    img_urls = []
    for css_url in css_urls:
        try:
            css_content = await fetch(css_url)
            img_urls.extend(extract_urls(BACKGROUND_IMAGE_PATTERN, css_content, css_url))
        except aiohttp.ClientError as e:
            logging.error(f"Error fetching CSS file {css_url}: {e}")
    return img_urls


async def find_all_images_on_page(url):
    try:
        html_content = await fetch(url)
        html_img_urls = find_images_from_html(html_content, url)
        css_urls = find_css_links(html_content, url)
        css_img_urls = await find_images_from_css_files(css_urls)
        all_img_urls = html_img_urls + css_img_urls
        return all_img_urls
    except aiohttp.ClientError as e:
        logging.error(f"Error fetching the webpage: {e}")
        return []
        