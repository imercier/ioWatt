import re
import requests
import json

url = "https://www.infoclimat.fr/observations-meteo/temps-reel/marseille-samena/000BL.html?graphiques"
test_str = requests.get(url).text
regex = (r"var _data_gr = (.*).$\n")
matches = re.finditer(regex, test_str, re.MULTILINE)
for match in matches:
    d = json.loads(match.group(1))
    break
print(d['srad'])
