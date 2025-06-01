
from __future__ import annotations
from requests import get

from RequestMaker import *
from HTMLParser import *

BASE_URL: str = "https://fr.wikipedia.org"

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

r = get("https://fr.wikipedia.org/wiki/P%C3%A9rou_aux_Jeux_olympiques_d%27%C3%A9t%C3%A9_de_2024")

