import requests
import re
from bs4 import BeautifulSoup
import lxml.html as html1
from lxml.html.clean import Cleaner
urls=[
#'http://www.icdrilling.com'
#,'http://www.hollyfrontier.com'
#,'http://www.hpinc.com'				###  more depth level
#,'http://www.halliburton.com'		###  parsing error at the end but ok
#,'http://www.globalp.com'			###   stupid url #waste

#,'http://glorienergy.com'		###   proper

#,'http://www.crc.com'				###  more depth level
#,'http://www.billbarrettcorp.com/opportunities/current-openings/'			### stupid url
#,'http://www.basware.com'			###   stupid url 
#,'http://www.ballard.com'			###  more depth level

#,'http://www.c-a-m.com'			###		shitty website
#,'http://www.tataatsu.com'
#,'http://www.calumetspecialty.com'		### ok ok
#,'http://www.cabotog.com'			### proper
#,'http://www.callon.com'			### no career page
#,'http://www.bkep.com'		### pdfs - career page
#,
'http://www.aeti.com'				### proper
#,'http://www.alphanr.com'		### stupid url  	###shitty website
#,'http://alphanr.mua.hrdepartment.com'		### stupid url
#,'http://www.apachecorp.com'	###  parsing error at the end but ok
#,'http://www.archcoal.com'		### last ink wrong
]
ill = 0
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
job=re.compile('.*about.*',re.IGNORECASE)
desc_link=[]
crawledLink=[]


for url in urls:
	ill=ill+1
	with open('link%i.txt'%ill,"w") as outfile:
		pass
	with open('link%i.txt'%ill,"a") as outfile:
		def crawl(link1):
			print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
			try:
				html=requests.get(link1)
				soup1=BeautifulSoup(html.content)
				for l in soup1.find_all('a'):
					print l.get('href')
					if job.match(str(l.get('href'))) and not str(l.get('href')) in crawledLink:
						l1=l.get('href')
						crawledLink.append(l1)
						if not linkPattern.match(l1):
							if l1[0]!='/':
								l1=url+'/'+l1
							else:
								l1=url+l1
							
						#print l1
						desc_link.append(l1)
						#a=crawl(l1)
						print "ddddddddddddddddddddddddddddddddddddddddddddddddddd"
			except:
				pass


		try:
			shtml=requests.get(url)

			desc_link=[]
			career_links=[]
			soup = BeautifulSoup(shtml.content)
			for link in soup.find_all('a'):
				print link.get('href')
				if job.match(str(link.get('href'))):
					print "tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
					link1=link.get('href')
					
					if not linkPattern.match(link1):
						if link1[0]!='/':
							link1=url+'/'+link1
						else:
							link1=url+link1
					if not link1 in crawledLink:
						crawledLink.append(link1)
						a=crawl(link1)
		except:
			pass
		print desc_link
		import urllib
		textss=[]
		for url in desc_link:
			if len(url)<100:
				outfile.write(" { ")
				try:
					cleaner=Cleaner()
					cleaner.javascript=True
					cleaner.style=True
					#htmla = cleaner.clean_html(html1.parse(url)).xpath('//p//text()')
					htmlb = cleaner.clean_html(html1.parse(url)).xpath('//div//text()')
					html=htmlb#+htmlb
					for t in html:
						t=re.sub(r'\n|\t|\r|  ','',t)
						if len(t)>30:
							print str(len(t)) + " " + t
							outfile.write(" , \n")
							outfile.write(t.encode("utf-8"))
				except:
					print "ERROR with " + str(url)
				outfile.write(" } \n")
