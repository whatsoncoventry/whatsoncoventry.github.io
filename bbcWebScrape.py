from bs4 import BeautifulSoup
import requests
"""BBC Coventry and Warwickshire Scrape"""
def getTopStoryBBC():
	"""Function to get BBC's Coventry and Warwickshire top story. Returns an array of two elements; 0th = title, 1st = contents"""
	topStory = []
	response = requests.get('https://www.bbc.co.uk/news/england/coventry_and_warwickshire')
	siteContent = BeautifulSoup(response.content, 'html.parser')
	articleTitles = siteContent.find_all('span', {'class' : 'title-link__title-text'}) #Look for specific title 'span' for article title
	articleContents = siteContent.find_all('p', {'class' : 'skylark__summary'}) #Look for specific summary paragraph for article paragraphs
	topStory.append(articleTitles[0].text) 
	topStory.append(articleContents[0].text)
	return topStory
#Example usage
x = getTopStoryBBC()
print(' - '.join(x))
