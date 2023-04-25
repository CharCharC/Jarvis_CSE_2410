import bs4
import urllib.request

def wotd(int_, input_):
   url = "https://www.merriam-webster.com/word-of-the-day" # The site where word is scraped 

   response = urllib.request.urlopen(url) # Create a request using beautifulsoup4
   doc = bs4.BeautifulSoup(response, features="lxml") # Assign response to a variable 

   content_div = doc.find_all("h2", class_="word-header-txt") # Scanned for html header that held the word 

   if int_==1:
      return True

   definition = doc.find_all("p") # Scanned for definition header

   definition_choice = input_ # Prompt user using Jarvis API

   if definition_choice.lower() == "y": # Change user input to lowercase so it's case insensitive
      return True
   else:
      return False
    