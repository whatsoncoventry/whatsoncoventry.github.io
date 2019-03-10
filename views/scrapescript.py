#!usr/bin/python3
#Daniel Jones
#import sqlite3 #Possible sqlite3 conversion
import json
from bs4 import BeautifulSoup
import requests
import datetime
now = datetime.datetime.now()
lastupdate = now.strftime("%d-%m-%Y %H:%M")
"""Functions to webscrape useful information from relevant target sites"""
def get_top_story_bbc():
	"""Function to get BBC's Coventry and Warwickshire top story. Returns an array of two elements where the first it the top story title and the second the contents"""
	topStory = []
	response = requests.get('https://www.bbc.co.uk/news/england/coventry_and_warwickshire')
	bbcContent = BeautifulSoup(response.content, 'html.parser')
	topStory.append(bbcContent.findAll('span', {'class' : 'title-link__title-text'})[0].text) 
	topStory.append(bbcContent.findAll('p', {'class' : 'skylark__summary'})[0].text)
	return topStory
def get_updates_cusu():
	"""Function to get the CUSU most recent updates and stories"""
	events = []
	times = []
	locations = []
	descriptions = []
	images = []
	data = ""
	response = requests.get('https://www.cusu.org/coventry')
	cusuContent = BeautifulSoup(response.content, 'html.parser')
	for event in cusuContent.findAll('a',{'class':'msl_event_name'}):
		events.append("<p style='font-weight:bold;'>"+event.text+"</p>") #Titles
	for date in cusuContent.findAll('dd',{'class':'msl_event_time'}):
		times.append("<li> When: "+date.text+"</li> <br />") #Dates
	for location in cusuContent.findAll('dd',{'class':'msl_event_location'}):
		locations.append("<li> Where: "+location.text+"</li> <br />") #Locations
	for description in cusuContent.findAll('dd',{'class':'msl_event_description'}):
		descriptions.append(description.text+"<br /> <br />") #Descriptions
	for image in cusuContent.findAll('span',{'class':'msl_event_image'}):
		images.append("<img src = '"+"https://www.cusu.org"+image.img['src']+"' style='width:480px;height:270px;'> <br />") #Image links
	results = zip(images,events,times,locations,descriptions)
	for result in results:
		data+=(' '.join(result))
	return data
def get_university_news():
	"""Returns a string of posts with links and dates from the CUMoodle 'University News' section"""
	response = requests.get('https://cumoodle.coventry.ac.uk')
	moodleContent = BeautifulSoup(response.content, 'html.parser')
	postLinks =[]
	headings = []
	dates = []
	data = ""
	for title in moodleContent.findAll('div',{'class':'subject'}):
		headings.append(title.text+"</a></p>")
	for link in moodleContent.findAll('div',{'class':'link'}):
		postLinks.append("<p style = 'font-size:120%;'> <a href = '"+link.a['href']+"'>") 
	for date in moodleContent.findAll('div',{'class':'author'}):
		dates.append("<p style='font-size:90%;'>"+date.text[18:]+"</p>")
	results = zip(postLinks, headings, dates)
	for result in results:
		data+=(''.join(result))
	return data
if __name__ == '__main__':
	#Example usage
	bbcStory = get_top_story_bbc()
	cusuUpdate = get_updates_cusu()
	moodleUpdate = get_university_news()
	bbcStoryToWeb = ' - '.join(list(bbcStory))
	
	"""with open('data.json', 'w') as fp:
					json.dump(bbcStory, fp, indent=4) 							#json incorporation
					for i in range(len(cusuUpdate)):
						json.dump(cusuUpdate[i].tolist(), fp, indent=4)
					json.dump(moodleUpdate, fp, indent=4)"""
			
	webpage = '''<!DOCTYPE HTML>
<html>
	<head>
		<title>What's On Coventry</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<meta name="description" content="" />
		<meta name="keywords" content="" />
		<link rel="stylesheet" href="css/main.css" />
	</head>
    <body class="is-preload">
        <!-- Header -->
        <header id="header">
            <a class="logo" href="/">What's On Coventry</a>
        <!-- Nav -->
        	<nav>
        <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/events">Events</a></li>
                <li><a href="/visit">Visit</a></li>
                <li><a href="/news">News and Updates</a></li>
            
        </ul>
        </nav>
        </header>

        <!-- Heading -->
        <div id="heading">
            <h1 style="font-weight:bold;">News and Updates</h1>
        </div>
		

        <!-- Main -->
        <section id="main" class="wrapper">
            <div class="inner">
                <div class="content">
                    <header>
                        <p style="font-size:200%; text-align:center;">Coventry's latest news, events, and updates all in once place</p>
                        <p style="text-align:center;">Last updated: {lastupdate}</p>
                        
						<hr>
                    </header>
                    
					<center>
					<a href="https://www.bbc.co.uk/news/england/coventry_and_warwickshire"> <img class="responsive" src="images/bbcnews.png" alt="BBC Coventry and Warwickshire" style='width:380px;height:170px;'> </a> </center>
                     <p style="font-size:120%; font-weight:bold;">{bbcTop}</p>
                    	<hr />
                    	
                    <h6 style="font-size:200%; text-align:center; font-weight:bold;" >Student Union News</h6>
                  		
                     <ul><p style="font-size:120%;">{cusuUpdate}</p></ul>
						<hr />
					<h6 style="font-size:200%; text-align:center; font-weight:bold;" >Coventry University News</h6>
                  		
                     <ul>{moodleUpdate}</ul>
                     
                     
						<hr />
					<a href="https://github.com/DanielJ0nes/Web-Scraper">This page is powered by a Python script written and developed by Daniel Jones</a>
                </div>
                
            </div>
        </section>

        <footer id="footer">
            <div class="inner">
                <div class="content">
                    <section>
                        <h3>About the project</h3>
                        <p>What's on Coventry is a project brought to you by Daniel Jones, Adam Smith, Jennifer Wan, Ricards Veveris, Thomas Walczak, Ross Woolfenden, Razcan Danciulescu and Ridvan Karaman. We aim to bring you a fast, convenient, and effective way of getting the most recent and accurate information about the city and university of Coventry</p>
                    </section>

                    <section>
                        <h4>Social media</h4>
                        <ul class="plain">
                            <li><a href="https://twitter.com/WhatOnCoventry"><i class="icon fa-twitter">&nbsp;</i>Twitter</a></li>
                            <li><a href="https://www.facebook.com/Whats-On-Coventry-1960577907395132"><i class="icon fa-facebook">&nbsp;</i>Facebook</a></li>
                            <li><a href="#"><i class="icon fa-instagram">&nbsp;</i>Instagram</a></li>
                            <li><a href="https://www.youtube.com/watch?v=WagR3jaBW34"><i class="icon fa-youtube">&nbsp;</i>YouTube</a></li>
                        </ul>
                    </section>
                </div>
                <div class="copyright">
                    &copy; Coventry University
                </div>
            </div>
        </footer>

        <!-- Scripts -->
        <script src="assets/js/jquery.min.js"></script>
        <script src="assets/js/browser.min.js"></script>
        <script src="assets/js/breakpoints.min.js"></script>
        <script src="assets/js/util.js"></script>
        <script src="assets/js/main.js"></script>
		<script type="text/javascript">function add_chatinline(){{var hccid=72962215;var nt=document.createElement("script");nt.async=true;nt.src="https://mylivechat.com/chatinline.aspx?hccid="+hccid;var ct=document.getElementsByTagName("script")[0];ct.parentNode.insertBefore(nt,ct);}}
add_chatinline(); </script>

    </body>
</html>
			'''.format(bbcTop=bbcStoryToWeb, moodleUpdate=moodleUpdate, cusuUpdate=cusuUpdate,lastupdate=lastupdate)		
	with open('news.hbs', 'w') as htmlPage:
		htmlPage.write(webpage)				
	htmlPage.close()
	print("built")
	"""conn = sqlite3.connect('webscraper.db') #Sql test
				sql = conn.cursor()
				sql.execute("INSERT INTO BBCTopStory (Article) VALUES (?)",[bbcStory])			#SQL incorporation
				conn.commit()
				sql.close()
				conn.close"""
