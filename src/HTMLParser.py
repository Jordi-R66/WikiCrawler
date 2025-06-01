from __future__ import annotations
from re import *

class Site:
	def __init__(self, smallUrl: str, title: str, parent: Site):
		self.url: str = smallUrl
		self.title: str = title
		self.parents: set[Site] = set()

		if parent != None and type(parent) == Site:
			self.parents.add(parent)
		else:
			self.parents = None

	def __eq__(self, value) -> bool:
		if (type(value) != Site):
			raise ValueError("Can't compare Site to non-Site objects")
		else:
			return self.url == value.url

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
			invalidHrefs.add(href)

	hrefs.difference_update(invalidHrefs)

	return hrefs