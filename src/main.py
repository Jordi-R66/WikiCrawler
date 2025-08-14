from requests import get
from json import *

from HTMLParser import *

from time import time

BASE_URL: str = "https://fr.wikipedia.org"
FIRST_URL: str = "/wiki/Montesquieu-des-Albères".replace(BASE_URL, "")
FIRST_TITLE: str = ""

VISITED: set[str] = set()
TO_VISIT: set[str] = set()
ALL_URLS: set[str] = set()

CORRESPONDANCE: dict[str: Site] = {}
SUIVANTS: dict[str: set[str]] = {}

phrases: set[str] = set()

corpus = open("corpus.txt", "w")


if __name__ == '__main__':
	TO_VISIT.add(FIRST_URL)

	start, stop = 0.0, 0.0
	limit: int = 500

	run = len(VISITED) < limit and len(TO_VISIT) > 0

	try:
		start = time()
		while run:
			smallUrl: str = TO_VISIT.pop()

			url = f"{BASE_URL}{smallUrl}"

			r = get(url)
			print(url, f"\n{"-"*len(url)}")

			if (r.status_code != 200):
				raise Exception(f"Couldn't get {smallUrl}")
			else:
				VISITED.add(smallUrl)

			html = r.text

			title: str = getTitle(html)

			hrefs: set[str] = getValidURLs(html)
			phrases.update(set(getValidSentences(html)))

			for p in phrases:
				corpus.write(f"{p}\n")

			phrases.clear()

			if (smallUrl == FIRST_URL):
				FIRST_TITLE = title

			currentSite: Site = Site(smallUrl, title)

			CORRESPONDANCE[smallUrl] = currentSite
			SUIVANTS[smallUrl] = set(hrefs)

			TO_VISIT.update(hrefs)
			TO_VISIT.difference_update(VISITED)

			run = len(VISITED) < limit and len(TO_VISIT) > 0
	except Exception as e:
		print(e)
	finally:
		stop = time()

		ALL_URLS.update(TO_VISIT)
		ALL_URLS.update(VISITED)

		print(f"{len(ALL_URLS)-1} découvertes en {stop-start} secondes\n")

		for k in SUIVANTS:
			SUIVANTS[k] = list(SUIVANTS[k])

		fp = open(FIRST_TITLE+".json", "w")
		fp.write(dumps(SUIVANTS, indent=4))
		fp.close()

		corpus.close()
