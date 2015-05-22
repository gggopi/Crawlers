import requests
import re
from bs4 import BeautifulSoup
import lxml.html as html1
from lxml.html.clean import Cleaner
from goose import Goose
from commonregex import CommonRegex
urls=[



#,'http://www.murphyoilcorp.com'					###		working
#,'http://www.millerenergyresources.com'			###		working
#,'http://www.midstatespetroleum.com'			###		working		### needs visible-text search selection
#,'http://www.nabors.com'					###		same problem as hollyfrontier 		### imp stuff inside 'form'
#,'http://www.nov.com'					###		same problem as hollyfrontier 		### imp stuff inside 'form' ###also unmatch word 'sustainability'
#,'http://www.ngsgi.com'				###		not working ### needs visible-text search selection
#,'http://www.nrplp.com'					###		not working ### needs visible-text search selection
#,'http://www.newconceptenergy.com'		### 	working  but website has less content

#,'http://www.matadorresources.com'		###		working
#,'http://www.markwest.com'				###		working
#,'http://www.magellanlp.com'				###		same problem as hollyfrontier 		### imp stuff inside 'form' 
#,'http://www.lucasenergy.com'			### 	working
#,'http://www.linnco.com'				### 	working
#,'http://www.lilisenergy.com'			### 	working
#'http://www.laredopetro.com'			#### working
#,'http://www.kosmosenergy.com'			### 	working
#,'http://www.philips.co.in'			### too much data output  ###needs to be refined
#,'http://www.icdrilling.com'			###		working
#,'http://www.hollyfrontier.com'		### need to be worked on
#,'http://www.hpinc.com'				###  ok ok
#,
'http://www.halliburton.com'		###  same problem as hollyfrontier  ###working but shitty output

#,'http://glorienergy.com'		###   proper ### working
#,'http://www.noblecorp.com'		###	   working
#,'http://www.crc.com'				###  working
#,'http://www.ballard.com'			###  more depth level   ####loads of shit  ### ok ok 		### working
#,'http://www.ntenergy.com'			### working
#,'http://www.c-a-m.com'			###		shitty website ## ok ok 
#,'http://www.tataatsu.com'			### dont even try
#,'http://www.calumetspecialty.com'		### loads of shit  				###	ok ok
#,'http://www.cabotog.com'			### working but check it
#,'http://www.callon.com'			### no career page			###	working
#,'http://www.bkep.com'		 ###proper	
#,'http://www.aeti.com'				### proper			### working
#,'http://www.alphanr.com'		###proper	
#,'http://www.apachecorp.com'	###  too much data output  ###needs to be refined
#,'http://www.archcoal.com'		### working but check it
]
ill = 0
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
job=re.compile('.*team.*|.*contact.*|.*about.*|.*management.*|.*directors.*',re.IGNORECASE)
job_okok=re.compile('.*team.*|.*contact.*|.*about.*|.*management.*|.*directors.*|.*governance.*',re.IGNORECASE)
unwanted=re.compile('.*join.*|.*mailto.*|.*pdf.*|.*recruit.*|.*events?.*|.*facts.*|.*mission.*|.*values.*|.*faq.*|.*news.?r?.*|.*career.*|.*updates.*|.*history.*|.*vision.*|.*award.*|.*products.*|.*polic(y|ies).*|.*feedback.*|.*support.*|.*innovaitons.*',re.IGNORECASE)
## NOTE: word 'resources removed from 'unwanted  and 'governance' is added.. add 'how.?.?we' = 1 add safety= 2
lang=re.compile('.*japanese.*|.*mandarin.*|.*portuguese.*|.*germen.*|.*french.*|.*twitter.*|.*linkedin.*|.*google.*',re.IGNORECASE)
err=re.compile('.*runtime.?error.*|.*403.?.?forbidden.*|.*not.?found.*',re.IGNORECASE)
desc_link=[]
crawledLink=[]
word_pattern = re.compile('([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+[a-z]+)?(?:\s+[A-Z][a-z]+)+)')
#self.contiguous_words = re.findall(word_pattern,self.article.text) 
depth_level=0
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
						l1=str(l.get('href'))
						print l1
						if not linkPattern.match(l1):
							if l1[0]!='/':
								l1=url+'/'+l1
							else:
								l1=url+l1

						if (job_okok.match(l1) or job_okok.match(l.get_text())) and  not ( unwanted.match(l1) or unwanted.match(l.get_text())) and not lang.match(l1) and not l1 in crawledLink:
							crawledLink.append(l1)								
							#print l1
							if not l1 in desc_link:
								desc_link.append(l1)
							a=crawl(l1)
				print "ddddddddddddddddddddddddddddddddddddddddddddddddddd"
			except:
				print "ERROR with " + link1


		try:
			shtml=requests.get(url)

			desc_link=[]
			career_links=[]
			soup = BeautifulSoup(shtml.content)
			for link in soup.find_all('a'):
				link1=link.get('href')
				print link1
				if (job_okok.match(str(link.get('href'))) or job_okok.match(link.get_text()))and not (unwanted.match(link1) or unwanted.match(link.get_text())) and not lang.match(link1):
					print "tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
					if not linkPattern.match(link1) :
						if link1[0]!='/':
							link1=url+'/'+link1
						else:
							link1=url+link1
					if not link1 in crawledLink:
						crawledLink.append(link1)
						depth_level=0
						desc_link.append(link1)
						a=crawl(link1)
		except:
			pass
		print desc_link
		if len(desc_link)==0:
			desc_link.append(url)
		import urllib
		textss=[]
		for url in desc_link:
			if len(url)<100 and job.match(url) and  not unwanted.match(url) and not lang.match(url):
				#outfile.write(" { ")
				try:
					html = requests.get(url)    
					raw = BeautifulSoup(html.content)
					#print raw.get_text()
					print str(len(raw('video')))+ "   " + str(len(raw('form'))) + "  " + str(len(raw('input'))) +" " + url
					# NOTE: set imput len limit 15or14. but one site had many as 26-proper one only.
					if err.match(str(raw('title'))) or err.match(str(raw('text'))):
						print "server error with "+url
						continue
#					print "form lenth = " + str(len(raw('form')))
					if len(raw('form'))>2:
						print "form lenth = " + str(len(raw('form'))) + "\n url= " + url
						continue
					for s in raw('style'):
						s.extract()
					for s in raw('script'):
						s.extract()
					for s in raw('input'):
						s.extract()					
					text=re.sub(r"\n\n\n",' ',raw.get_text())
					try:
						outfile.write(text.encode('utf-8'))
					except:
						print "encode ERROR"					
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