import requests
import re
from bs4 import BeautifulSoup
import lxml.html as html1
urls=[
#'http://www.c-a-m.com'
#,'http://www.tataatsu.com'
#,'http://www.calumetspecialty.com'		### ok ok
#,
'http://www.cabotog.com'			### proper
#,'http://www.callon.com'			### no career page
#,'http://www.bkep.com',		### pdfs - career page
,
'http://www.aeti.com'				### proper
#,'http://www.alphanr.com'		### stupid url
#
#,'http://alphanr.mua.hrdepartment.com'		### stupid url
,'http://www.apachecorp.com'	###  parsing error at the end but ok
#,
#'http://www.archcoal.com'		### last ink wrong
]
ill = 0
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
job=re.compile('.*career.*|.*job.*|.*posting.*',re.IGNORECASE)

crawledLink=[]

for url in urls:
	ill=ill+1
	with open('%i.txt'%ill,"w") as outfile:
		pass
	with open('%i.txt'%ill,"a") as outfile:
		shtml=requests.get(url)
		desc_link=[]
		career_links=[]
		soup = BeautifulSoup(shtml.content)
		for link in soup.find_all('a'):
			#print link.get('href')
			if job.match(str(link.get('href'))):
				#print "tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
				link1=link.get('href')
				
				if not linkPattern.match(link1):
					link1=url+link1
				if not link1 in crawledLink:
					crawledLink.append(link1)
					html=requests.get(link1)
					soup1=BeautifulSoup(html.content)
					print soup1.title
					for l in soup1.find_all('a'):
						
						if job.match(str(l.get('href'))) and not str(l.get('href')) in crawledLink:
							l1=l.get('href')
							crawledLink.append(l1)
							#print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
							if not linkPattern.match(l1):
								l1=url + l1
							print l1
							desc_link.append(l1)

#print "2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222"
		print desc_link
		import urllib
		textss=[]
		for url in desc_link:
			outfile.write(" { ")
			htmla = html1.parse(url).xpath('//p/text()')
			htmlb = html1.parse(url).xpath('//li/text()')
			html=htmla+htmlb
			for t in html:
				if len(t)>15:
					outfile.write(" , ")
					outfile.write(t.encode("utf-8"))
					#outfile.write(" \n ")
			outfile.write(" } \n")

# with open("data.txt","a") as outfile:
# 	for t in textss:
# 		outfile.write()
# 		outfile.write(textss)
	
