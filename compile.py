#! /usr/bin/env python3
'''
Compile summary file(s)
'''

# imports
from glob import glob
from json import dump as jdump
from html import escape

# main program
if __name__ == "__main__":
    # create REFS.json
    REFS = dict()
    for fas in glob('*/*.fas'):
        ID = fas.split('/')[-2].strip()
        if ID in REFS:
            raise ValueError("Duplicate ID: %s" % ID)
        REFS[ID] = {
            'name': open('%s/%s.name.txt' % (ID,ID)).read().strip(),
            'shortname': [l.strip() for l in open('%s/%s.shortname.txt' % (ID,ID)).read().strip().splitlines()],
        }
    f = open('REFS.json', 'w'); jdump(REFS, f); f.close()

    # create index.html
    html = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reference Genomes</title>
<style>
body { font-family: sans-serif; margin: 2rem; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 0.5rem; text-align: left; vertical-align: top; }
th { background: #f6f8fa; }
tr:nth-child(even) { background: #fafafa; }
</style>
</head>
<body>
<h1>Reference Genomes</h1>
<table>
<thead>
<tr>
<th>ID</th>
<th>Name</th>
<th>Short Name(s)</th>
</tr>
</thead>
<tbody>
'''
    for ID in sorted(REFS):
        html += '''<tr>
<td><a href="https://github.com/Niema-Lab/Reference-Genomes/tree/main/%s">%s</a></td>
<td>%s</td>
<td>%s</td>
</tr>
''' % (
            escape(ID),
            escape(ID),
            escape(REFS[ID]['name']),
            escape(', '.join(REFS[ID]['shortname']))
        )
    html += '''</tbody>
</table>
</body>
</html>
'''
    f = open('index.html', 'w'); f.write(html); f.close()
