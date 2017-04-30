from django import template
from places.models import Place

register = template.Library()

@register.filter(name='linkPlace')
def linkPlace(place_id):
	#return "ID is {id}".format(id=str(place_id))
	"""Function takes a place ID and, if it refers to a place withits own page, returns text with a hyperlink."""
	if not place_id:
		return ''
	try:
		place = Place.objects.get(id=place_id)
	except:
		return 'Unknown place'
	place_name='{t}, {c}'.format (t=place.town, c=place.county)
	if not place.detail:
		return place_name
	return "<a href='/places/{p_id}.html'>{p}</a>".format(p_id=place_id, p=place_name)

