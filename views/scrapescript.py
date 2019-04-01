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

#Example usage
bbcStory = get_top_story_bbc()
cusuUpdate = get_updates_cusu()
moodleUpdate = get_university_news()
bbcStoryToWeb = ' - '.join(list(bbcStory))	
			
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
					<li><a href="/discovery">Discovery</a></li>            
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
						<a href="https://www.bbc.co.uk/news/england/coventry_and_warwickshire">
						<img class="responsive" src="images/bbcnews.png" alt="BBC Coventry and Warwickshire" style='width:380px;height:170px;'> </a> 
					</center>
                	     		<p style="font-size:120%; font-weight:bold;">{bbcTop}</p>
                	    		<hr>
                    	
                	    		<h6 style="font-size:200%; text-align:center; font-weight:bold;" >Student Union News</h6>
                  		
    					 <ul>
					 	<p style="font-size:120%;">{cusuUpdate}</p>
					</ul>
					<hr>
					<h6 style="font-size:200%; text-align:center; font-weight:bold;" >Coventry University News</h6>
                  		
                	     		<ul>{moodleUpdate}</ul>
                     
                     
					<hr>
					<a href="https://github.com/DanielJ0nes/Web-Scraper">This page is powered by a Python script written and developed by Daniel Jones</a>
                		</div>
            		</div>
        	</section>
	
		<!-- CTA -->
		<section id="cta" class="wrapper">
			<div class="inner">
        		        <div class="newsletter">
					<h3>Sign up to our newsletter</h3>
                    			<form id="newsletter" action="/news" onsubmit="subscribed()" method="get">
		    				Firstname:
							<input type="text" placeholder="Name" name="name" required
							pattern = "[A-Za-z]{1,20}$" maxlength="20"><br>
                        			E-mail:
							<input type="text" placeholder="E-mail address" name="email" required
							pattern = "[a-z0-9]+@[a-z0-9]+\.[a-z]{2,}$"><br>
                        			<input class="subscribe" type="submit" value="Subscribe">                        
                    			</form>
                    		</div>
			</div>

        		<footer id="footer">
            			<div class="inner">
        				<div class="content">
                    				<section>
                        				<h3>About the project</h3>
                        				<p>What's on Coventry is a project brought to you by Daniel Jones, Adam Smith, Jennifer Wan, Ricards Veveris, Thomas Walczak, Ross Woolfenden, Razcan Danciulescu and Ridvan Karaman. We aim to bring you a fast, convenient, and effective way of getting the most recent and accurate information about the city and university of Coventry</p>
                    				</section>
                    				<section>
							<h4>Our Social media Accounts : </h4>
							<ul class="plain">
                               	 				<a href="https://www.youtube.com/watch?v=WagR3jaBW34" class="fa fa-youtube">  </a>
                              					<a href="https://twitter.com/WhatOnCoventry" class="fa fa-twitter">   </a>
                                				<a href="https://www.facebook.com/Whats-On-Coventry-1960577907395132" class="fa fa-facebook">   </a>
                                				<a href="https://www.instagram.com/Whats-On-Coventry-1960577907395132" class="fa fa-instagram">   </a>			
							</ul>
						</section>
                			</div>
                			<div class="copyright">
                    				&copy; Coventry University
                			</div>
            			</div>
        		</footer>
		</section>
		
        <!-- Scripts -->
        <script src="assets/js/jquery.min.js"></script>
        <script src="assets/js/browser.min.js"></script>
        <script src="assets/js/breakpoints.min.js"></script>
        <script src="assets/js/util.js"></script>
        <script src="assets/js/main.js"></script>
	<script type="text/javascript">function add_chatinline(){{var hccid=72962215;var nt=document.createElement("script");nt.async=true;nt.src="https://mylivechat.com/chatinline.aspx?hccid="+hccid;var ct=document.getElementsByTagName("script")[0];ct.parentNode.insertBefore(nt,ct);}}
	add_chatinline(); </script>
	<script>
		function subscribed(){
			alert("Thank you for subscribing")
		}
	</script>

    </body>
</html>
	'''.format(bbcTop=bbcStoryToWeb, moodleUpdate=moodleUpdate, cusuUpdate=cusuUpdate,lastupdate=lastupdate)
with open('views/news.hbs', 'w') as htmlPage:
	htmlPage.write(webpage)				
htmlPage.close()
print("built")
