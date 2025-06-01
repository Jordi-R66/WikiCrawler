import re

def getTitle(html: str) -> str:
	correspondance: str = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)

	

def getValidURLs(html: str) -> set[str]:
	hrefs = set(re.findall(r'<a[^>]+href=["\']?([^"\'>\s]+)', html, re.IGNORECASE))
	invalidHrefs = set()

	for href in hrefs:
		isValid: bool = href.startswith("/wiki/") and not (":" in href)

		if not isValid:
			invalidHrefs.add(href)

	hrefs.difference_update(invalidHrefs)

	return hrefs