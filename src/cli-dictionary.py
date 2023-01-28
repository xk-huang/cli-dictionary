#!/usr/bin/python3
import os
import sys

import iterfzf as fzf

from args import Args
from config.words import words
from config.api import API as API_CONFIG
from config.languages import DEFAULT_LANG
from printer import Printer
from api import API

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

def get_results(word: str, lang: str, sy: bool, ex: bool) -> None:
	if lang in API_CONFIG.keys():
		url = API_CONFIG[lang] + word
		print_definition(url, sy, ex)
	else:
		Printer.lang_not_found()


def print_meanings(meaning, iter_num):
	partOfSpeech : str = meaning['partOfSpeech']

	text = '[bold][white]{}. {}[/white][/bold]'.format(iter_num, partOfSpeech.upper())
	Printer.default_print(text)

	definitions = meaning['definitions']

	for idx, definition in enumerate(definitions, 1):
		text = '\t[green]{}. {}[/green]'.format(idx, definition['definition'])

		if definition.get('example', None):
			text = text + '\n\t\texample: {}'.format(definition['example'])
		if definition.get('synonyms', None):
			text = text + '\n\t\tsynonyms: {}'.format(", ".join(definition['synonyms']))
		if definition.get('antonyms', None):
			text = text + '\n\t\tantonyms: {}'.format(", ".join(definition['antonyms']))

		Printer.default_print(text)

	if meaning.get('synonyms', None):
		text = '\tsynonyms: {}'.format(', '.join(meaning['synonyms']))
		Printer.default_print(text)

	if meaning.get('antonyms', None):
		text = '\tantonyms: {}'.format(', '.join(meaning['antonyms']))
		Printer.default_print(text)


def print_definition(url, sy, ex):
	api = API(url)
	print(url)
	data = api.get_response()

	try:
		word = data[0]['word']
	except:
		Printer.default_print('[red]{}[/red]'.format(data))
		return

	if data[0].get('phonetic', None):
		phonetic = data[0]['phonetic']
	elif data[0].get('phonetics', None):
		for _phonetic in data[0]['phonetics']:
			if _phonetic.get('text', None):
				phonetic = _phonetic['text']
				break
	else:
		phonetic = '?'
	Printer.default_print('[bold][white]{}: {}[/white][/bold]'.format(word, phonetic))

	meanings = data[0]['meanings']
	for index, meaning in enumerate(meanings, 1):
		print_meanings(meaning, index)

def main(word, args):
	lang = os.getenv('CLI_DICT_DEFAULT_LANG', DEFAULT_LANG)

	if word == '' or word == None:
		Printer.default_print("[red]Default argument 'word' is missing \n")

		Printer.default_print("How you should use: ")
		Printer.default_print("-> cli-dictionary [bold][white]<word>[/bold][/white] [white]<lang>[/white]")
		return
	#	word = fzf.iterfzf(words)

	synonyms = args['synonyms']
	examples = args['examples']

	lang = args['lang'] if args['lang'] != '' else lang
	lang = lang.upper()

	get_results(word, lang, synonyms, examples)

if __name__ == '__main__':
	parser = Args.get_parser()
	args = vars(parser.parse_args())
	word = args['word']
	main(word, args)
