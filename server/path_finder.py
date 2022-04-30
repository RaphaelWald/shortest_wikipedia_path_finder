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
                mid_links = _get_all_links(link[0])
                print(mid_links)
                link_lists[-1] = link_lists[-1] + mid_links
                for mid_link in mid_links:

                    for i in range(shortest_path_length):
                        for backlink in backlink_lists[i]:
                            if mid_link[0] == backlink[0]:
                                shortest_path_length = i + 1
                                path = _get_full_path(link_lists,
                                                      backlink_lists,
                                                      mid_link[0], mid_link[1],
                                                      backlink[1])
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
                mid_links = _get_all_backlinks(backlink[0])
                print(mid_links)
                backlink_lists[-1] = backlink_lists[-1] + mid_links
                for mid_link in mid_links:
                    for i in range(shortest_path_length):
                        for link in link_lists[i]:
                            if mid_link[0] == link[0]:
                                shortest_path_length = i + 1
                                path = _get_full_path(link_lists,
                                                      backlink_lists,
                                                      mid_link[0], link[1],
                                                      mid_link[1])
                                paths.append(path)
                        if i == shortest_path_length:
                            break

            if paths:
                return paths
            else:
                return bi_bfs_recursion(link_lists, backlink_lists, True,
                                        i + 1)

    return bi_bfs_recursion([[(source, "start")]], [[(destination, "end")]],
                            True, 0)


def print_paths(paths):
    for path in paths:
        for link in path:
            if link == path[-1]:
                print(link)
            else:
                print(f"{link} -> ", end="")


def _get_all_links(page):
    LINKS_PARAMS["titles"] = page
    R = S.get(url=URL, params=LINKS_PARAMS)
    DATA = R.json()

    PAGES = DATA["query"]["pages"]

    links = []

    for k, v in PAGES.items():
        if "links" in v.keys():
            for l in v["links"]:
                links.append((l["title"], page))

    if "continue" in DATA.keys():
        LINKS_PARAMS["plcontinue"] = DATA["continue"]["plcontinue"]
        links = links + _get_all_links(page)
    return links


def _get_all_backlinks(page):
    BACKLINKS_PARAMS["bltitle"] = page
    R = S.get(url=URL, params=BACKLINKS_PARAMS)
    DATA = R.json()

    BACKLINKS = DATA["query"]["backlinks"]
    backlinks = []

    for b in BACKLINKS:
        backlinks.append((b["title"], page))

    if "continue" in DATA.keys():
        BACKLINKS_PARAMS["blcontinue"] = DATA["continue"]["blcontinue"]
        backlinks = backlinks + _get_all_backlinks(page)

    return backlinks


def _get_full_path(link_lists, backlink_lists, mid_link, pre, suc):
    path = [mid_link]
    current_pre = pre
    while current_pre != "start":
        print(current_pre)
        for links in link_lists:
            for link in links:
                if current_pre == link[0]:
                    path.insert(0, current_pre)
                    current_pre = link[1]

    current_suc = suc
    while current_suc != "end":
        for backlinks in backlink_lists:
            for backlink in backlinks:
                if current_suc == backlink[0]:
                    path.append(current_suc)
                    current_suc = backlink[1]

    return path