from requests import get
from json import *

from RequestMaker import *
from HTMLParser import *

BASE_URL: str = "https://fr.wikipedia.org"
FIRST_URL: str = "/wiki/Sc%C3%A8ne_(cin%C3%A9ma)"

VISITED: set[str] = set()
TO_VISIT: set[str] = set()

CORRESPONDANCE: dict[str: Site] = {}
SUIVANTS: dict[str: set[str]] = {}

if __name__ == '__main__':
	TO_VISIT.add(FIRST_URL)

	limit: int = 1000

	run = len(VISITED) < limit and len(TO_VISIT) > 0

	while run:
		smallUrl: str = TO_VISIT.pop()
		VISITED.add(smallUrl)

		url = f"{BASE_URL}{smallUrl}"

		r = get(url)
		html = r.text

		title: str = getTitle(html)
		hrefs: set[str] = getValidURLs(html)

		currentSite: Site = Site(smallUrl, title)

		CORRESPONDANCE[smallUrl] = currentSite
		SUIVANTS[smallUrl] = set(hrefs)

		TO_VISIT.update(hrefs)
		TO_VISIT.difference_update(VISITED)

		print(smallUrl)

		run = len(VISITED) < limit and len(TO_VISIT) > 0

	fp = open(FIRST_URL+".json", "w")
	fp.write(dumps(SUIVANTS, indent=4))
	fp.close()