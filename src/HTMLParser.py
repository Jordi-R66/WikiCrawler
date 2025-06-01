from __future__ import annotations
from re import *

class Site:
	def __init__(self, smallUrl: str, title: str):
		self.url: str = smallUrl
		self.title: str = title
		self.parents: set[Site] = set()

	def __eq__(self, value) -> bool:
		if (type(value) not in (Site, str)):
			raise ValueError("Can't compare Site to non-Site objects")
		else:
			if (type(value) == Site):
				return self.url == value.url
			else:
				return self.url == value

def getTitle(html: str) -> str:
	correspondance: list[str] = findall(r'<title[^>]*>(.*?)</title>', html, IGNORECASE | DOTALL)

	if len(correspondance) == 0:
		return ""
	else:
		return correspondance[0]

def getValidURLs(html: str) -> set[str]:
	hrefs = set(findall(r'<a[^>]+href=["\']?([^"\'>\s]+)', html, IGNORECASE))
	invalidHrefs = set()

	for href in hrefs:
		isValid: bool = href.startswith("/wiki/") and not (":" in href)

		if not isValid:
			href = href.split("#")[0]
			invalidHrefs.add(href)

	hrefs.difference_update(invalidHrefs)

	return hrefs