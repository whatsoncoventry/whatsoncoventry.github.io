"""jonesd37"""
from bs4 import BeautifulSoup
import requests
"""BBC Coventry and Warwickshire Scrape"""


def getTopStoryBBC():
	"""Function to get BBC's Coventry and Warwickshire top story. Returns an array of two elements; 0th = title, 1st = contents"""
	topStory = []
	response = requests.get('https://www.bbc.co.uk/news/england/coventry_and_warwickshire')
	soup = BeautifulSoup(response.content, 'html.parser')
	articleTitles = soup.find_all('span', {'class' : 'title-link__title-text'})
	articleContents = soup.find_all('p', {'class' : 'skylark__summary'})
	topStory.append(articleTitles[0].text)
	topStory.append(articleContents[0].text)
	return topStory


#Example usage
x = getTopStoryBBC()
print(' - '.join(x))





