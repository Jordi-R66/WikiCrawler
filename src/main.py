from requests import get
from json import *

from RequestMaker import *
from HTMLParser import *

from time import time

BASE_URL: str = "https://fr.wikipedia.org"
FIRST_URL: str = "/wiki/Sc%C3%A8ne_(cin%C3%A9ma)"
FIRST_TITLE: str = ""

VISITED: set[str] = set()
TO_VISIT: set[str] = set()
ALL_URLS: set[str] = set()

CORRESPONDANCE: dict[str: Site] = {}
SUIVANTS: dict[str: set[str]] = {}

if __name__ == '__main__':
	TO_VISIT.add(FIRST_URL)

	start, stop = 0.0, 0.0
	limit: int = 1000

	run = len(VISITED) < limit and len(TO_VISIT) > 0

	try:
		start = time()
		while run:
			smallUrl: str = TO_VISIT.pop()

			url = f"{BASE_URL}{smallUrl}"

			r = get(url)

			if (r.status_code != 200):
				raise Exception(f"Couldn't get {smallUrl}")
			else:
				VISITED.add(smallUrl)

			html = r.text

			title: str = getTitle(html)
			hrefs: set[str] = getValidURLs(html)

			if (smallUrl == FIRST_URL):
				FIRST_TITLE = title

			currentSite: Site = Site(smallUrl, title)

			CORRESPONDANCE[smallUrl] = currentSite
			SUIVANTS[smallUrl] = set(hrefs)

			TO_VISIT.update(hrefs)
			TO_VISIT.difference_update(VISITED)

			print(smallUrl)

			run = len(VISITED) < limit and len(TO_VISIT) > 0
	except:
		print("Erreur survenue")
	finally:
		stop = time()

		ALL_URLS.update(TO_VISIT)
		ALL_URLS.update(VISITED)

		print(f"{len(ALL_URLS)} découverts en {stop-start:.3} secondes\n")

		for k in SUIVANTS:
			SUIVANTS[k] = list(SUIVANTS[k])

		fp = open(FIRST_TITLE+".json", "w")
		fp.write(dumps(SUIVANTS, indent=4))
		fp.close()