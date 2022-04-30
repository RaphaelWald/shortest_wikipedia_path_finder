"""This module implements the bidirectional algorithm to find the shortest paths f"""

import requests

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
    "bltitle": "Placeholder",
    "bllimit": "max",
}

start = "Pietro Lombardi (singer)"
end = "Helene Fischer"


def bidirectional_BFS(source, destination):

    def bi_bfs_recursion(link_lists, backlink_lists, forward, i):
        paths = []
        if forward:
            links = link_lists[-1]
            link_lists.append([])
            shortest_path_length = len(backlink_lists)
            for link in links:
                mid_links = _get_all_links(link)
                link_lists[-1] = link_lists[-1] + mid_links
                for mid_link in mid_links:

                    for i in range(shortest_path_length):
                        for backlink in backlink_lists[i]:
                            if mid_link[0] == backlink[0]:
                                shortest_path_length = i + 1
                                path = mid_link[-2::-1] + backlink
                                paths.append(path)
                        if i == shortest_path_length:
                            break

            if paths:
                return paths
            else:
                return bi_bfs_recursion(link_lists, backlink_lists, False,
                                        i + 1)

        else:
            backlinks = backlink_lists[-1]
            backlink_lists.append([])
            shortest_path_length = len(link_lists)
            for backlink in backlinks:
                mid_links = _get_all_backlinks(backlink)
                backlink_lists[-1] = backlink_lists[-1] + mid_links
                for mid_link in mid_links:
                    for i in range(shortest_path_length):
                        for link in link_lists[i]:
                            if mid_link[0] == link[0]:
                                shortest_path_length = i + 1
                                path = link[-2::-1] + mid_link
                                paths.append(path)
                        if i == shortest_path_length:
                            break

            if paths:
                return paths
            else:
                return bi_bfs_recursion(link_lists, backlink_lists, True,
                                        i + 1)

    link_lists, backlink_lists = [], []
    link_lists.append([[source]])
    backlink_lists.append([[destination]])

    return bi_bfs_recursion(link_lists, backlink_lists, True, 0)


def print_paths(paths):
    for path in paths:
        for link in path:
            if link == path[-1]:
                print(link)
            else:
                print(f"{link} -> ", end="")


def _get_all_links(path):
    print(path)
    page = path[0]
    LINKS_PARAMS["titles"] = page
    R = S.get(url=URL, params=LINKS_PARAMS)
    DATA = R.json()

    PAGES = DATA["query"]["pages"]

    links = []

    for k, v in PAGES.items():
        if "links" in v.keys():
            for l in v["links"]:
                links.append([l["title"]] + path)

    if "continue" in DATA.keys():
        LINKS_PARAMS["plcontinue"] = DATA["continue"]["plcontinue"]
        links = links + _get_all_links(path)
    return links


def _get_all_backlinks(path):
    print(path)
    page = path[0]
    BACKLINKS_PARAMS["bltitle"] = page
    R = S.get(url=URL, params=BACKLINKS_PARAMS)
    DATA = R.json()

    BACKLINKS = DATA["query"]["backlinks"]
    backlinks = []

    for b in BACKLINKS:
        backlinks.append([b["title"]] + path)

    if "continue" in DATA.keys():
        BACKLINKS_PARAMS["blcontinue"] = DATA["continue"]["blcontinue"]
        backlinks = backlinks + _get_all_backlinks(path)

    return backlinks