import requests
import re
from bs4 import BeautifulSoup
urls=[
# 'http://www.c-a-m.com'
# #,
# #'http://www.tataatsu.com'
# ,'http://www.calumetspecialty.com'		### ok ok
# ,
# 'http://www.cabotog.com'
# #,'http://www.callon.com'			### no career page
# #,'http://www.bkep.com',		### pdfs - career page
# ,
'http://www.aeti.com'
# #,'http://www.alphanr.com'		### stupid url
# #
# #,'http://alphanr.mua.hrdepartment.com'		### stupid url
# ,'http://www.apachecorp.com'
#,
#'http://www.archcoal.com'
]
ill = 0
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
job=re.compile('.*career.*|.*job.*|.*posting.*',re.IGNORECASE)
career_links=[]
crawledLink=[]
desc_link=[]
for url in urls:
	ill=ill+1
	with open('%i.txt'%ill,"a") as outfile:
		shtml=requests.get(url)
		#soup = BeautifulSoup(shtml)
		soup = BeautifulSoup(shtml.content)
		#soup.prettify()
		#print soup.prettify()
		#print soup.get_text()
		#global job#=re.compile('.*career.*|.*job.*|.*posting.*',re.IGNORECASE)

		for link in soup.find_all('a'):
			#print link.get('href')
			if job.match(str(link.get('href'))):
				#print "tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
				link1=link.get('href')
				
				if not linkPattern.match(link1):
					link1=url+link1
				#print link1
				career_links.append(link1)
				#print career_links


	#for link in career_links:
				
				if not link1 in crawledLink:
					crawledLink.append(link1)
					html=requests.get(link1)
					soup1=BeautifulSoup(html.content)
					print soup1.title
					for l in soup1.find_all('a'):
						
						if job.match(str(l.get('href'))):
							l1=l.get('href')
							#print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
							if not linkPattern.match(l1):
								l1=url + l1
							print l1
							desc_link.append(l1)


	##
#print "2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222"
# del desc_link[-1]
		print desc_link
		import urllib
		textss=[]
		for url in desc_link:
			outfile.write(" { ")
			html = urllib.urlopen(url).read()
			soup = BeautifulSoup(html)
			texts = soup.findAll(text=True)

			def visible(element):
			    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
			        return False
			    elif re.match('<!--.*-->', unicode(element)):
			        return False
			    return True

			visible_texts = filter(visible, texts)
			for t in visible_texts:
				if len(t)>15:
					outfile.write(" , ")
					outfile.write(t.encode("utf-8"))
					#outfile.write(" \n ")
			outfile.write(" } \n")

# with open("data.txt","a") as outfile:
# 	for t in textss:
# 		outfile.write()
# 		outfile.write(textss)
	
