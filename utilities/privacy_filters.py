from django.conf import settings

def sanitize(query):
    """Goes through a query and checks all the person fields to see if that person is marked as private.
    If so, it sets the person foreign key to 0"""

    if not settings.PRIVACY:
        return query
    for item in query:
        if item.person_id and item.person.private:
            item.person_id=0
    return query

def sp_filter(query):
    if not settings.PRIVACY:
        return query
    return  (x for x in query if not x.private)

def people_filter(query):
    if not settings.PRIVACY:
        return query
    return  query.filter(private=False)
