from django.shortcuts import render
from datetime import datetime


# Create your views here.

from .models import PlainPage

def renderpage(request, url):
    thepage = PlainPage.objects.get(url = url)
    if thepage.template=='main':
        n = datetime.now()
        t = n.timetuple()
        y, m, d, h, min, sec, wd, yd, i = t
        month = n.strftime("%b")
        thepage.content+='<hr>&copy;{yr} Stephen West<br>\
            This version of the site generated {d} {m} {yr}'.format(yr=y, d=d, m=month)
    context = {'pagedata': thepage}
    return render(request, 'plainpages/page.html', context)
