import requests
import re
from bs4 import BeautifulSoup
urls=[
'http://www.aeti.com',
'http://www.alphanr.com'
,
'http://www.apachecorp.com',
'http://www.archcoal.com'
]
career_links=[]
for url in urls:
	shtml=requests.get(url)
	#soup = BeautifulSoup(shtml)
	soup = BeautifulSoup(shtml.content)
	#soup.prettify()
	#print soup.prettify()
	#print soup.get_text()
	job=re.compile('.*career.*|.*job.*',re.IGNORECASE)

	for link in soup.find_all('a'):
		#print link.get('href')
		if job.match(str(link.get('href'))):
			print "tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
			link1=link.get('href')
			linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
			if not linkPattern.match(link1):
				link1=url+link1
			print link1
			career_links.append(link1)
print career_links