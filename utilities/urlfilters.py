from django import template

import re
pattern = re.compile(r'\{\{([\w\s,\-\'\.]+)\|person\|(\w+)\}\}')
h1_pattern = re.compile(r'\<\s*[hH]1')
h2_pattern = re.compile(r'\<\s*[hH]2')
h3_pattern = re.compile(r'\<\s*[hH]3')
ref_pattern = re.compile(r'\[\@(\w+)\]')

def preparse (item):
	#Parse the text, looking for patterns of the form {{ab c|person|d1234efg}}
	# convert to <a href="/people/d1234efg.html">ab c</a>
	item = re.sub(ref_pattern, r'<a href="/people/\1.html">[\1]</a>', item)
	return re.sub(pattern, r'<a href="/people/\2.html">\1 (\2)</a>', item)

def book_preparse (item):
	#Parse the text, looking for patterns of the form {{ab c|person|d1234efg}}
	# convert to ab c [d1234efg]
	item = re.sub(ref_pattern, r'[\1]', item)
	return re.sub(pattern, r'\1 [\2]', item)

def heading_down (item):
	#Parse text looking for html heading tags and downgrade them
	item = re.sub(h3_pattern, r'<h5', item)
	item = re.sub(h2_pattern, r'<h4', item)
	item = re.sub(h1_pattern, r'<h3', item)	
	return item
