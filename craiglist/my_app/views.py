import requests
from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models
import urllib
# Create your views here.

def index(request):
    return render(request,'base.html',{})
def new_search(request):
    search = request.POST.get('search')
    city = request.POST.get('city')
    searchd = {'query':search}
    BASE_URL = 'https://{}.craigslist.org/search/?'.format(city.lower())
    final_url = BASE_URL+ urllib.parse.urlencode(searchd)
    
    try:
        response = requests.get(final_url)
        data = response.text
        soup = BeautifulSoup(data,'html.parser')
        data1 = soup.find_all('li', {'class':'result-row'})
        postinglist = []
        for d in data1:
            post_title= d.find('a',{'class':'result-title hdrlnk'}).text 
            post_url = d.find('a',{'class':'result-title hdrlnk'})['href']
            if( d.find('span',{'class':'result-price'}) ):
                post_price = d.find('span',{'class':'result-price'}).text
            else:
                post_price = 'N/A'
            if(d.find('a',{'class':'result-image gallery'})):
                img_url = d.find('a',{'class':'result-image gallery'})['href']
            else:
                img_url= None
                print(img_url)
            postinglist.append((post_title,post_url,post_price))
        models.Search.objects.create(search=search)
        print(data1[2])
        context = {'search':search,'postinglist':postinglist}
    except requests.ConnectionError as exception:
        context={'error':exception}
    return render(request,'my_app/new_search.html',context)



