from __future__ import annotations
from html import unescape
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
		return " ".join(correspondance[0].split(" ")[0:-2])

def getValidURLs(html: str) -> set[str]:
	hrefs = set(findall(r'<a[^>]+href=["\']?([^"\'>\s]+)', html, IGNORECASE))
	invalidHrefs = set()

	for href in hrefs:
		isValid: bool = href.startswith("/wiki/") and not (":" in href)

		if not isValid:
			invalidHrefs.add(href)

	hrefs.difference_update(invalidHrefs)

	hrefs = {href.split("#")[0] for href in hrefs}

	return hrefs

def getValidSentences(html: str) -> set[str]:
	html = unescape(html)

	match = search(r'<div\s+class="mw-content-ltr mw-parser-output"(.*?)>(.*?)</div>', html, flags=DOTALL)
	if not match:
		return set()
	div_content = match.group(2)

	# 2️⃣ Supprimer scripts et styles
	html = sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=IGNORECASE | DOTALL)

	# 3️⃣ Remplacer <img> par leur alt (texte alternatif)
	html = sub(r'<img[^>]*alt=["\']([^"\']+)["\'][^>]*>', r' \1 ', html, flags=IGNORECASE)

	# 4️⃣ Forcer un séparateur après les blocs de texte
	html = sub(r'</(p|h[1-6]|div)>', r'.</\1>', html, flags=IGNORECASE)

	# 5️⃣ Supprimer toutes les balises HTML restantes
	html = sub(r'<[^>]+>', '', html)
	html = sub(r'(?:↑\s*)?(?:[a-zA-Z]\s+){3,}[a-zA-Z](?:\s*\([^\)]*\))?', '', html)

	# 6️⃣ Supprimer contenu entre crochets ou accolades
	html = sub(r'\[[^\]]*\]|\{[^}]*\}', '', html)

	# 7️⃣ Supprimer les fragments d’URL
	html = sub(r'https?://\S+|www\.\S+|/\S+\.\S+', '', html)

	# 8️⃣ Réduire les espaces multiples
	texte_pur = sub(r'\s+', ' ', html).strip()

	# 9️⃣ Séparer en phrases
	phrases_brut = [p.strip() for p in split(r'[.!?]+', texte_pur) if p.strip()]

	# 🔟 Filtrer le bruit : longueur mini + présence de mots
	phrases = list(p for p in phrases_brut if len(p) > 3 and search(r'[A-Za-zÀ-ÖØ-öø-ÿ]{2,}', p) )
	print(*phrases, sep="\n\n")
	return phrases