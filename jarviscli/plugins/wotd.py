from plugin import plugin
import bs4
import urllib.request

@plugin("wotd")
def wotd(jarvis, s):
    url = "https://www.merriam-webster.com/word-of-the-day" # The site where word is scraped 

    response = urllib.request.urlopen(url) # Create a request using beautifulsoup4
    doc = bs4.BeautifulSoup(response, features="lxml") # Assign response to a variable 

    content_div = doc.find_all("h2", class_="word-header-txt") # Scanned for html header that held the word 

    jarvis.say("\nThe Merriam Webster word of the day is "+content_div[0].get_text().title()) # Print value using Jarvis API, index 0 because we only want first value

    definition = doc.find_all("p") # Scanned for definition header

    definition_choice = jarvis.input("\nWould you like to see the definition? (Y/N)\n") # Prompt user using Jarvis API

    if definition_choice.lower() == "y": # Change user input to lowercase so it's case insensitive
        jarvis.say("\nAccording to the Merriam Webster online dictionary: "+definition[0].get_text()) # Print using Jarvis API, again only want first value in the find all command
    else:
        jarvis.say("Have a great day!")
    