#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja_markdown import MarkdownExtension
from collections import defaultdict
import os

OUTPUT = 'out'

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
env.add_extension(MarkdownExtension)


people = ['Alexis Arlène',
          'Benoit Caillet',
          'Dominique Eav',
          'Gaëlle',
          'Joan Plassard',
          'Tristan Forrièrre']

results = [{ 'date': '13/10/2020',
             'results': [{'w': 'Benoit Caillet', 'l': 'Dominique Eav'},
                         {'w': 'Joan Plassard', 'l': 'Gaëlle'}] },
           {'date': '20/10/2020',
            'results': [{'w': 'Dominique Eav', 'l': 'Tristan Forrièrre'},
                        {'w': 'Alexis Arlène', 'l': 'Dominique Eav'}]}]

class Stats(dict):
    def __init__(self):
        for name in people:
            self[name] = { 'score': 0,
                           'nbwins': 0,
                           'nbgames': 0 }
    def rankings_by(self, key):
        groups = defaultdict(list)
        for name in self:
            groups[self[name][key]].append(name)
        grouplist = [(score, ', '.join(people)) for score, people in groups.items()]
        grouplist.sort(key=lambda entry: entry[0], reverse=True)
        return grouplist

stats = Stats()

for session in results:
    for result in session['results']:
        stats[result['w']]['score'] += 3
        stats[result['w']]['nbwins'] += 1
        stats[result['w']]['nbgames'] += 1
        stats[result['l']]['score'] += 1
        stats[result['l']]['nbgames'] += 1



template = env.get_template('index.html')
with open(os.path.join(OUTPUT, f"index.html"), 'w') as f:
    f.write(template.render(stats=stats, results=results))
print('Pages generated')
