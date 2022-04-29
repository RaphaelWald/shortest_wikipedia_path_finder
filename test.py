#!/usr/bin/python3
"""
    get_links.py

    MediaWiki API Demos
    Demo of `Links` module: Get all links on the given page(s)

    MIT License
"""

import requests
import time

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

LINKS_PARAMS = {
    "action": "query",
    "format": "json",
    "titles": "Placeholder",
    "prop": "links",
    "pllimit": "max",
}

BACKLINKS_PARAMS = {
    "action": "query",
    "format": "json",
    "list": "backlinks",
    "bltitle": "Werder Bremen",
    "bllimit": "max",
}

start = "Pietro Lombardi (singer)"
end = "Helene Fischer"


def get_all_links(page):
    LINKS_PARAMS["titles"] = page
    R = S.get(url=URL, params=LINKS_PARAMS)
    DATA = R.json()

    PAGES = DATA["query"]["pages"]

    links = []

    for k, v in PAGES.items():
        if "links" in v.keys():
            for l in v["links"]:
                links.append(l["title"])

    if "continue" in DATA.keys():
        LINKS_PARAMS["plcontinue"] = DATA["continue"]["plcontinue"]
        links = links + get_all_links(page)
    return links


def get_all_backlinks(page):
    BACKLINKS_PARAMS["bltitle"] = page
    R = S.get(url=URL, params=BACKLINKS_PARAMS)
    DATA = R.json()

    BACKLINKS = DATA["query"]["backlinks"]
    backlinks = []

    for b in BACKLINKS:
        backlinks.append(b["title"])

    if "continue" in DATA.keys():
        BACKLINKS_PARAMS["blcontinue"] = DATA["continue"]["blcontinue"]
        backlinks = backlinks + get_all_backlinks(page)

    return backlinks


def rec(link_lists, backlink_lists, forward, i):
    paths = []
    if forward:
        links = link_lists[-1]
        link_lists.append([])
        shortest_path_length = len(backlink_lists)
        for link in links:
            mid_links = get_all_links(link)
            link_lists[-1] = link_lists[-1] + mid_links
            for mid_link in mid_links:

                for i in range(shortest_path_length):
                    if mid_link in backlink_lists[i]:
                        shortest_path_length = i + 1
                        path = get_path(link_lists, backlink_lists, mid_link)
                        paths.append(path)
                        break

        if paths:
            return paths
        else:
            return rec(link_lists, backlink_lists, False, i + 1)

    else:
        backlinks = backlink_lists[-1]
        backlink_lists.append([])
        shortest_path_length = len(link_lists)
        for backlink in backlinks:
            mid_links = get_all_backlinks(backlink)
            backlink_lists[-1] = backlink_lists[-1] + mid_links
            for mid_link in mid_links:

                for i in range(shortest_path_length):
                    if mid_link in link_lists[i]:
                        shortest_path_length = i + 1
                        path = get_path(link_lists, backlink_lists, mid_link)
                        paths.append(path)
                        break

        if paths:
            return paths
        else:
            return rec(link_lists, backlink_lists, True, i + 1)


def bidirectional_BFS(source, destination):
    return rec([[source]], [[destination]], True, 0)


def get_path(link_lists, backlink_lists, mid_link):
    return mid_link


t0 = time.perf_counter()

paths = bidirectional_BFS(start, end)
print(paths)
t1 = time.perf_counter()
print(t1 - t0)
