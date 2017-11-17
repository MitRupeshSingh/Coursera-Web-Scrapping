
#import the library
import bs4
import re
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup

# get the url for coursera with range of pages to be crawled
urls = ['https://www.coursera.org/courses?_facet_changed_=true&languages=en&primaryLanguages=en&start=%s' % page for page in xrange(200,224,20)]

#loop through all the pages
for url in urls:

        #save the result in coursera.csv
	savefile=open("coursera.csv","a")
	uClient = uReq(url)
	page_html = uClient.read()
	uClient.close()
	page_soup=soup(page_html, "html.parser")
	hrefArrays = []
	containers=page_soup.findAll("a",{"data-click-key":"catalog.search.click.offering_card"})
	inputTag=page_soup.findAll('a',{"href":True})

	# check if the course is about specialization or not and append it
	for source in inputTag:
		if (source['href'].find('/learn',0,8)!=-1):
			hrefArrays.append(source['href'])
		elif (source['href'].find('/specialization',0,18)!=-1):
			hrefArrays.append(source['href'])
			
	i=0
	for container in containers:
		img_source = container.div.div.div.img["src"]
		course_title = container.div.find("div",{"class":"offering-info flex-1"}).h2

		#save course title name and img source
		savefile.write(course_title.text.encode("utf-8").replace(",","|")+","+img_source)		
		course_specialization = container.div.find("span",{"class":"specialization-course-count"})


		#check for specialization and save it
		if(course_specialization!=None):                        
			savefile.write(","+course_specialization.text+",")
		else:
			savefile.write(","+",")


		#check for partners with the course and save it
		partners_name = container.div.find("div",{"class":"text-light offering-partner-names"})
		if(partners_name==None):
			savefile.write(container.find("span",{"class":"text-light offering-partner-names"}).text.encode("utf-8").strip().replace(",","|")+",")
		else:
			savefile.write(partners_name.text.encode("utf-8").replace(",","|")+",")


                # go to rating page and save the rating result		
		next_url='https://www.coursera.org%s' %hrefArrays[i]
		savefile.write(next_url+",") 
		RatinguClient = uReq(next_url)
		rating_html = RatinguClient.read()
		RatinguClient.close()
		rating_soup=soup(rating_html, "html.parser")
		rating_container=rating_soup.findAll("div",{"class":"ratings-info"})
		for url_rate in rating_container:
			rating_name = url_rate.find("div",{"class":"ratings-text bt3-hidden-xs"})
			rating_name.text.encode("utf-8").replace("Average User Rating ","")
			rating_name.text.encode("utf-8").replace("See what learners said","")
			savefile.write(rating_name.text.encode("utf-8").replace("Average User Rating ","").replace("See what learners said",""))
		savefile.write("\n")
		i=i+1
		
		
