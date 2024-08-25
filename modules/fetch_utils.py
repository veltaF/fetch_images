from urllib.parse import urlparse, urljoin
import aiohttp
import re

def is_valid_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ("http", "https") and parsed_url.netloc != ""


def extract_urls(pattern, html_content, base_url):
    found_urls = re.findall(pattern, html_content)
    return [urljoin(base_url, url) for url in found_urls]


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
            