#!/usr/bin/env python3
import chevron
from random import randint, random
from pathlib import Path

from fetch import fetch_memorials


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
			'text_width': self.width * 0.65,
			'text_x': self.width / 4.5,
			'text_y': self.width / 5.5
		}
		return chevron.render(template, data)

	def height(self):
		return self.width * (431 / 441) # dimensions of image

	def bottom(self):
		return self.y + self.height()


def gen_tombstone(memorial, x, y):
	name, cause, is_player = memorial
	if is_player:
		size = 350
	else:
		size = 200
		#cause = None
	return Tombstone(
		x=x, 
		y=y + 300 + randint(0, 100),
		size=size,
		name=name,
		cause=cause
	)


def render(tstones, fo):
	tombstone_template = Path('tombstone.mustache').read_text()
	header = Path('header.html').read_text()
	footer = Path('footer.html').read_text()

	snippets = [t.render(tombstone_template) for t in tstones]

	print(header)
	for s in snippets:
		print(s)
	print(footer)


def convert_memorials_to_tombstones(memorials):
	memorials = list(memorials)
	y = 0
	x = randint(0, 5)
	for memorial in memorials:
		if x >= 800:
			x = randint(0, 25)
			y += 250
		tombstone = gen_tombstone(memorial, x, y)		
		x += (random() * 0.5 + 1) * tombstone.width
		yield tombstone


if __name__ == "__main__":
	tstones = convert_memorials_to_tombstones(fetch_memorials())
	tstones = sorted(tstones, key=lambda t: t.bottom())
	with open('output.html', 'w') as f:
		render(tstones, f)