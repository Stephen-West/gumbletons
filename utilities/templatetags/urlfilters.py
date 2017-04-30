from django import template

import re
pattern = re.compile(r'\{\{([\w\s,\-\'\.]+)\|person\|(\w+)\}\}')

def preparse (item):
	#Parse the text, looking for patterns of the form {{ab c|person|d1234efg}}
	# convert to <a href="/people/d1234efg.html">ab c</a>
	return re.sub(pattern, r'<a href="/people/\2.html">\1</a>', item)


