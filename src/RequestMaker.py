from requests import get

languages: list[str] = [
	"fr"
]

class RequestMaker:
	def __init__(self, lang: str):
		if  not (lang in languages):
			raise Exception("Unknown language")

		self.BASE_URL: str = f"{lang}.wikipedia.org/wiki/"
