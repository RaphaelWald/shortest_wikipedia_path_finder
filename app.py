import sys
import requests
import re
import time
import aiohttp
import asyncio

start_page = sys.argv[1].replace(" ", "_")
end_page = sys.argv[2].replace(" ", "_")
language = "en"

if len(sys.argv) > 3:
    language = sys.argv[3]

start_url = f"https://{language}.wikipedia.org/wiki/{start_page}"
end_url = f"https://{language}.wikipedia.org/wiki/{end_page}"


async def get_all(link):

    async with aiohttp.ClientSession() as session:

        for idx, link in enumerate(links):
            url = f"https://{language}.wikipedia.org{link}"
            print(idx)
            async with session.get(url) as resp:
                html = await resp.text()


start_html = requests.get(start_url).text
end_html = requests.get(end_url).text
A_HREF_REGEX = '<a href="/wiki/\S+"'

a_hrefs = re.findall(A_HREF_REGEX, start_html)
links = {a_href[9:-1] for a_href in a_hrefs}

start = time.perf_counter()
asyncio.run(get_all(links))
end = time.perf_counter()
print(end - start)