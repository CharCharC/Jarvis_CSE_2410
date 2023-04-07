from plugin import plugin
import bs4
import urllib.request

@plugin("wotd")
def wotd(jarvis, s):
    url = "https://www.merriam-webster.com/word-of-the-day"
    response = urllib.request.urlopen(url)
    doc = bs4.BeautifulSoup(response, features="lxml")
    content_div = doc.find_all("h2", class_="word-header-txt")
    jarvis.say("\nThe Merriam Webster word of the day is "+content_div[0].get_text().title())
    def_ = doc.find_all("p")
    def_choice = input("\nWould you like to see the definition?\n")
    if def_choice.lower() == "yes":
        jarvis.say("\nAccording to the Merriam Webster online dictionary: "+def_[0].get_text())
    