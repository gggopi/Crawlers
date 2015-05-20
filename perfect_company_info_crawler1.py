import requests
import re
from bs4 import BeautifulSoup
import lxml.html as html1
from lxml.html.clean import Cleaner
from goose import Goose
from commonregex import CommonRegex
urls=[
#'http://www.icdrilling.com'
#,'http://www.hollyfrontier.com'
#,'http://www.hpinc.com'				###  more depth level
#,'http://www.halliburton.com'		###  parsing error at the end but ok
#,'http://www.globalp.com'			###   stupid url #waste

#,'http://glorienergy.com'		###   proper
#,'www.newfld.com'
#,'http://www.noblecorp.com/'
#,'http://www.crc.com'				###  more depth level
#,'http://www.billbarrettcorp.com/opportunities/current-openings/'			### stupid url
#,'http://www.basware.com'			###   stupid url 
#,'http://www.ballard.com'			###  more depth level   ####loads of shit
#,'http://www.ntenergy.com/'
#,'http://www.c-a-m.com'			###		shitty website
#,'http://www.tataatsu.com'
#,'http://www.calumetspecialty.com'		### ok ok
#,'http://www.cabotog.com'			### proper
#,'http://www.callon.com'			### no career page
#,'http://www.bkep.com'		### pdfs - career page
#,'http://www.aeti.com'				### proper
#,'http://www.alphanr.com'		### stupid url  	###shitty website
#,'http://alphanr.mua.hrdepartment.com'		### stupid url
#,'http://www.apachecorp.com'	###  parsing error at the end but ok
#,'http://www.archcoal.com'		### last link wrong
]
ill = 0
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
job=re.compile('.*team.*|.*contact.*|.*about.*|.*management.*',re.IGNORECASE)
unwanted=re.compile('.*join.*|.*pdf.*|.*recruit.*|.*fact.*|.*mission.*|.*values.*|.*career.*|.*history.*',re.IGNORECASE)
desc_link=[]
crawledLink=[]
word_pattern = re.compile('([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+[a-z]+)?(?:\s+[A-Z][a-z]+)+)')
#self.contiguous_words = re.findall(word_pattern,self.article.text) 
depth_level=0
#seen=set()
for url in urls:
	ill=ill+1
	with open('link%i.txt'%ill,"w") as outfile:
		pass
	with open('link%i.txt'%ill,"a") as outfile:
		def crawl(link1):
			print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
			try:
				global depth_level
				depth_level=depth_level+1
				if depth_level<=10:
					html=requests.get(link1)
					soup1=BeautifulSoup(html.content)
					for l in soup1.find_all('a'):
						print l.get('href')
						if job.match(str(l.get('href'))) and  not unwanted.match(str(l.get('href'))) and not str(l.get('href')) in crawledLink:
							l1=l.get('href')
							crawledLink.append(l1)
							if not linkPattern.match(l1):
								if l1[0]!='/':
									l1=url+'/'+l1
								else:
									l1=url+l1
								
							#print l1
							desc_link.append(l1)
							a=crawl(l1)
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
					
					if not linkPattern.match(link1) and not unwanted.match(link1):
						if link1[0]!='/':
							link1=url+'/'+link1
						else:
							link1=url+link1
					if not link1 in crawledLink:
						crawledLink.append(link1)
						depth_level=0
						a=crawl(link1)
		except:
			pass
		print desc_link
		if len(desc_link)==0:
			desc_link.append(url)
		import urllib
		textss=[]
		for url in desc_link:
			if len(url)<100:
				#outfile.write(" { ")
				try:

					# g=Goose()
					# art=g.extract(url=url)
					# text=art.cleaned_text.encode("utf-8")
					# print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
					# print text
					#outfile.write(text)
					html = requests.get(url)    
					raw = BeautifulSoup(html.content)  
					for s in raw('style'):
						s.extract()
					for s in raw('script'):
						s.extract()

					# parsed_text = CommonRegex(raw.get_text())
					# print parsed_text.phones
					# print parsed_text.emails
					# print parsed_text.street_addresses
					#global seen
					text=re.sub(r"\n\n\n",' ',raw.get_text())
					
					#seen.add(text)

					outfile.write(text.encode('utf-8'))
					
					#print parsed_text
				except:
					print "ERROR with " + str(url)
				outfile.write("  \n")
	with open('link%i.txt'%ill) as text:
	    with open('ulink%i.txt'%ill, 'w') as output:
	        seen = set()
	        for line in text:
	            line_hash = hash(line)
	            if line_hash not in seen:
	                output.write(line)
	                seen.add(line_hash)