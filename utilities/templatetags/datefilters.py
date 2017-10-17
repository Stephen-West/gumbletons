from django import template

register = template.Library()
monthlist = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

@register.filter(name='format_date')
def format_date(date):
	"""Function takes a date string and returns a human readable date.

	Date strings are probably in the form YYYY-MM-DD but may be in some other form"""
	if not date:
		return ''
	date=date.strip()
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	about = ""
	if date.startswith('?') or date.endswith('?'):
		about = "ca. "
		date= date.strip('?')
	elif date.startswith('<'):
		about = "Before "
		date= date.strip('<')
	elif date.startswith('>'):
		about = "After "
		date= date.strip('>')
	try:
		[year, month, day] = date.split('-')
		date_string = year
		month_ord=int(month)
		if month_ord>0 and month_ord<13:
			date_string = months[month_ord -1]+ " " + date_string
			day = day.lstrip('0')
			if day:
				date_string = day + " " + date_string
		date_string = about + date_string
		return date_string
	except:
		return about + date

@register.filter(name='year')
def format_date(date):
	"""Function takes a date string and returns a year.

	Date strings are probably in the form YYYY-MM-DD but may be in some other form"""
	if not date:
		return ''
	date=date.strip()
	about = ""
	if date.startswith('?') or date.endswith('?'):
		about = "ca. "
		date= date.strip('?')
	try:
		[year, month, day] = date.split('-')
		date_string = year
		date_string = about + date_string
		return date_string
	except:
		return about + date
