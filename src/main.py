
from requests import get

from RequestMaker import *
from HTMLParser import *

BASE_URL: str = "https://fr.wikipedia.org"



r = get("https://fr.wikipedia.org/wiki/P%C3%A9rou_aux_Jeux_olympiques_d%27%C3%A9t%C3%A9_de_2024")

html = r.text

print(getTitle(html))
print(getValidURLs(html))