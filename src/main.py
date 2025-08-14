from requests import get
from api import read_config, sendMsg
from json import *

from HTMLParser import *

from time import *

BASE_URL: str = "https://fr.wikipedia.org"
FIRST_URL: str = "/wiki/Langues_en_Europe".replace(BASE_URL, "")
FIRST_TITLE: str = ""

CARTO: bool = False
EXTRAC: bool = True

VISITED: set[str] = set()
TO_VISIT: set[str] = set()
ALL_URLS: set[str] = set()

CORRESPONDANCE: dict[str: Site] = {}
SUIVANTS: dict[str: set[str]] = {}

phrases: set[str] = set()
corpus: None = None

chars_lim: int = 1_000_000_000
chars_count = 0

if EXTRAC:
	corpus = open("corpus.txt", "w")

if __name__ == '__main__':
	TO_VISIT.add(FIRST_URL)

	start, stop = 0.0, 0.0
	limit: int = 65536

	#run = len(VISITED) < limit and len(TO_VISIT) > 0
	run: bool = chars_count < chars_lim and len(TO_VISIT) > 0

	read_config("tokens")

	try:
		start = time()
		while run:
			smallUrl: str = TO_VISIT.pop()

			url = f"{BASE_URL}{smallUrl}"

			r = get(url)
			#print(url, f"\n{"-"*len(url)}")

			if (r.status_code != 200):
				raise Exception(f"Couldn't get {smallUrl}")
			else:
				VISITED.add(smallUrl)

			html = r.text

			title: str = getTitle(html)

			hrefs: set[str] = getValidURLs(html)

			if EXTRAC:
				phrases.update(set(getValidSentences(html)))

				for p in phrases:
					corpus.write(f"{p}\n")
					chars_count += len(p)

				phrases.clear()

			if (smallUrl == FIRST_URL):
				FIRST_TITLE = title

			currentSite: Site = Site(smallUrl, title)

			CORRESPONDANCE[smallUrl] = currentSite
			SUIVANTS[smallUrl] = set(hrefs)

			TO_VISIT.update(hrefs)
			TO_VISIT.difference_update(VISITED)

			#run = len(VISITED) < limit and len(TO_VISIT) > 0
			run = chars_count < chars_lim and len(TO_VISIT) > 0
	except Exception as e:
		print(e)
	finally:
		stop = time()

		if EXTRAC:
			corpus.close()

		ALL_URLS.update(TO_VISIT)
		ALL_URLS.update(VISITED)

		output_str: str = f"[{strftime("%d-%m-%Y %H:%M:%S", localtime(stop))}]\n{len(ALL_URLS)-1} découvertes en {stop-start} secondes\n"

		print(output_str)
		sendMsg(output_str)

		for k in SUIVANTS:
			SUIVANTS[k] = list(SUIVANTS[k])

		if CARTO:
			fp = open(FIRST_TITLE+".json", "w")
			fp.write(dumps(SUIVANTS, indent=4))
			fp.close()
