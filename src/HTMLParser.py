from __future__ import annotations
from html import unescape
from bs4 import BeautifulSoup, Comment
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

def getValidSentences(html: str) -> list[str]:
	soup = BeautifulSoup(unescape(html), 'html.parser')

	# 1️⃣ Extraire uniquement la div "mw-content-ltr mw-parser-output"
	div_content = soup.find('div', class_='mw-content-ltr mw-parser-output')
	if not div_content:
		return []

	# 2️⃣ Réinitialiser le soup pour ne garder que cette div
	soup = BeautifulSoup(f'<div>{div_content}</div>', 'html.parser')

	# 3️⃣ Supprimer les éléments indésirables
	for element in soup.find_all(string=lambda text: isinstance(text, Comment)):
		element.extract()
	for infobox in soup.find_all('div', class_=lambda c: c and 'infobox' in c):
		infobox.decompose()
	for bandeau in soup.find_all('div', class_=lambda c: c and 'bandeau' in c):
		bandeau.decompose()
	for boite_grise in soup.find_all('div', class_=lambda c: c and 'boite-grise' in c):
		boite_grise.decompose()
	for navbox_container in soup.find_all('div', class_=lambda c: c and 'navbox-container' in c):
		navbox_container.decompose()
	for li in soup.find_all('li'):
		li.decompose()
	for table in soup.find_all('table'):
		table.decompose()
	for sup in soup.find_all('sup'):  # Supprime les références [1], [note 1]
		sup.decompose()
	for span in soup.find_all('span', class_=lambda c: c and ('reference' in c or 'mw-editsection' in c)):
		span.decompose()

	# 4️⃣ Remplacer les images par leur texte alternatif
	for img in soup.find_all('img'):
		if 'alt' in img.attrs:
			img.replace_with(f" {img['alt']} ")

	# 5️⃣ Supprimer les titres (h1-h6) et ajouter des séparateurs après les paragraphes
	for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
		tag.decompose()
	for p in soup.find_all('p'):
		p.append(" SEP ")

	# 6️⃣ Récupérer le texte brut
	texte_brut = soup.get_text(separator=' ', strip=True)

	# 7️⃣ Nettoyage agressif des artefacts
	texte_brut = sub(r'<\/[^>]+>"\}[^}]*}', '', texte_brut)  # Résidus JSON/JS
	texte_brut = sub(r'[A-Za-z]+\s*<\/[^>]+>[^}]*}', '', texte_brut)  # "couter</small>"}...
	texte_brut = sub(r'\"(?:data|classes)\"[^}]*}', '', texte_brut)  # Paires "data":...
	texte_brut = sub(r'[A-Za-z]+\s*<\/[^>]+>', '', texte_brut)  # "couter</small>"
	texte_brut = sub(r'[,\s]+\"[^"]*\":', '', texte_brut)  # Clés JSON
	texte_brut = sub(r'\[\s*[^\]]*\s*\]', '', texte_brut)  # Références [1]
	texte_brut = sub(r'\(\s*[^)]*\s*\)', '', texte_brut)  # Notes (note 1)
	texte_brut = sub(r'↑\s*[^.\n]*', '', texte_brut)  # Flèches ↑
	texte_brut = sub(r'\s*\[[^]]*\]\s*', ' ', texte_brut)  # Crochets résiduels
	texte_brut = sub(r'\s*\([^)]*\)\s*', ' ', texte_brut)  # Parentheses résiduelles
	texte_brut = sub(r'\s+', ' ', texte_brut)  # Espaces multiples

	texte_brut = sub(r'\[[^\]]*\]', '', texte_brut)  # Supprime tout entre crochets [ ... ]
	texte_brut = sub(r'\{[^}]*\}', '', texte_brut)  # Supprime tout entre accolades { ... }

	# 8️⃣ Découper en blocs et nettoyer la ponctuation
	blocs_texte = [
		sub(r'\s+([,.!?;])', r'\1', b.strip())  # Espace avant ponctuation
		.replace(" ,", ",")
		.replace(" .", ".")
		.replace("' ", "'")
		.replace(" :", ":")
		for b in texte_brut.split('SEP')
		if b.strip()
	]

	phrases = []
	for bloc in blocs_texte:
		# Découper le bloc en phrases (sur .!?)
		phrases_bloc = [
			p.strip() for p in split(r'(?<=[.!?])\s+', bloc)
			if p.strip() and len(p.split()) > 2  # Filtrer les phrases trop courtes
		]
		phrases.extend(phrases_bloc)

	#fp = open("page.html", "w")
	#fp.write(soup.prettify())
	#fp.close()
	#print(*phrases, sep="\n\n")
	return set(phrases)