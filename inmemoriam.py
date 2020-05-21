#!/usr/bin/env python3
import chevron
import math
import requests
from bs4 import BeautifulSoup
from io import StringIO
from random import randint
from pathlib import Path


class Tombstone:
	def __init__(self, x, y, size, name, cause):
		self.width = size
		self.x = x
		self.y = y - self.height()
		self.name = name
		self.cause = cause

	def render(self, template):
		data = {
			'x': self.x,
			'y': self.y,
			'width': self.width,
			'name': self.name,
			'cause': self.cause,
			'font': 12,
			'text_width': self.width * 0.5,
			'text_x': self.width / 4.5,
			'text_y': self.width / 5
		}
		return chevron.render(template, data)

	def height(self):
		return self.width * (521 / 800) # dimensions of image

	def bottom(self):
		return self.y + self.height()


def sawtooth(x):
	r = x % 100
	r /= 50
	if r < 1:
		y = r
	else:
		y = (1 + (1 - r)) - 0.1
	return y


def gen_tombstone(memorial, y):
	name, cause, is_player = memorial
	if is_player:
		size = 400
	else:
		size = 200
		cause = None
	return Tombstone(
		x=randint(0, 80), 
		y=y + 300,
		size=size,
		name=name,
		cause=cause
	)


def render(tstones, fo):
	tombstone_template = Path('tombstone.mustache').read_text()
	header = Path('header.html').read_text()
	footer = Path('footer.html').read_text()

	snippets = [t.render(tombstone_template) for t in tstones]

	fo.write(header)
	for s in snippets:
		fo.write(s)
	fo.write(footer)


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


def convert_memorials_to_tombstones(memorials):
	memorials = list(memorials)
	i = 0
	for memorial in memorials:
		yield gen_tombstone(memorial, i * 30)
		i += 1


if __name__ == "__main__":
	tstones = convert_memorials_to_tombstones(fetch_memorials())
	tstones = sorted(tstones, key=lambda t: t.bottom())
	with open('output.html', 'w') as f:
		render(tstones, f)