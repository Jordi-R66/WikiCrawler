from requests import post

config: dict[str: str] = {}

def read_config(token_file: str):
	fp = open(token_file, "r")

	lines: list[str] = fp.read().split("\n")

	print(lines)

	fp.close()

	for l in lines:
		params = l.split("=")
		config[params[0]] = params[1]

def sendMsg(msg: str) -> int:
	req = post("https://smsapi.free-mobile.fr/sendmsg", json={
		"user": config["USER"],
		"pass": config["API_KEY"],
		"msg": msg
	})

	return req.status_code