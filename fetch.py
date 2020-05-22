import requests
import re
from bs4 import BeautifulSoup

expedition_pattern = re.compile(r"\(expedition \d+\)")


def get_name(column):
	a = column.find("a")
	if a:
		return (a.string, True)
	else:
		return (column.string, False)


def get_cause(column):
	cause = column.string
	return expedition_pattern.sub('', cause)


def get_table():
	raw = requests.get('http://barrowmaze.wikidot.com/')
	soup = BeautifulSoup(raw.text, features="lxml")
	header = soup.find("span", string="Character Memorial")
	return header.parent.next_sibling.next_sibling.find("table")


def fetch_memorials():
	table = get_table()
	rows = table.find_all("tr")
	for row in rows[1:]:
		cols = row.find_all("td")
		name, is_player = get_name(cols[0])
		cause = get_cause(cols[2])
		yield (name.strip(), cause.strip(), is_player)