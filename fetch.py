import requests
from bs4 import BeautifulSoup


def fetch_memorials():
	raw = requests.get('http://barrowmaze.wikidot.com/')
	soup = BeautifulSoup(raw.text, features="lxml")
	header = soup.find("span", string="Character Memorial")
	table = header.parent.next_sibling.next_sibling.find("table")
	rows = table.find_all("tr")
	for row in rows[1:]:
		cols = row.find_all("td")
		a = cols[0].find("a")
		if a:
			name = a.string
			is_player = True
		else:
			name = cols[0].string			
			is_player = False
		cause = cols[2].string
		yield (name.strip(), cause.strip(), is_player)