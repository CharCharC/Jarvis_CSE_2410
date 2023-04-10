from plugin import plugin
import bs4
import urllib.request
from colorama import Fore


@plugin("stl_finder")
def stl_finder(jarvis, s):
    jarvis.say("Would you like to search for a model or view saved models\n")
    query = jarvis.input("(search/saved): ")
    if query == "search":
        search(jarvis,s)
    elif query == "saved":
        view_saved_models(jarvis, s)
    print("\n")
    
def search(jarvis, s):
    ROOT_URL = "https://thangs.com/search/"
    URL_END = "?scope=all"
    search_term = jarvis.input("What would you like to search for?\n")
    search_term = search_term.replace(" ", "_")
    url = ROOT_URL + search_term + URL_END
    models = get_models(url)
    counter = 0
    if len(models) == 0:
        jarvis.say("No results found")
        return
    jarvis.say("\nResults:")
    for i in range(3):
        jarvis.say(f"({str(counter+1)}) {models[counter]}")
        counter += 1

    yes = True
    while counter < len(models)-3 and yes:
        response = jarvis.input("\nWould you like to see more? (y/n): ")
        if response == 'y':
            for i in range(3):
                jarvis.say(f"({str(counter+1)}) {models[counter]}")
                counter += 1
        else:
            yes = False;
    response = jarvis.input("\nWould you like to save a model? (y/n): ")
    if response == 'y':
        model_number = int(jarvis.input("\nWhich model would you like to save: "))
        save_model(jarvis, s, models, model_number)

def get_models(url):
    response = urllib.request.urlopen(url)
    doc = bs4.BeautifulSoup(response, features="lxml")
    list_view = doc.find("div", class_ = "list-view")
    results = list_view.find("div", class_ = "")
    links = results.find_all("div", class_ = "SearchResult_ListView-0-2-225")
    models = []
    for link in links:
        href = link.find_all("a")[0]["href"]
        if href[0:4] == "http":
            models.append(href)
    return models

def save_model(jarvis, s, models, i):
    if i < 0 or i > len(models):
        jarvis.say("Invalid model number", Fore.RED)
        invalid = True
        while(invalid):
            i = int(jarvis.input("Please enter a new model number: "))
            if i > 0 and i < len(models):
                invalid = False
        
    with open("saved_models.txt", "a") as file:
        file.write(f"{models[i-1]}\n")
    jarvis.say(f"\nModel {i} has been saved")

def view_saved_models(jarvis, s):
    with open("saved_models.txt", 'r') as file:
        for i, link in enumerate(file):
            jarvis.say(f"({i}) {link}")
    answer = jarvis.input("Would you like to edit the list? (y/n): ")
    if answer is "y":
        answer = int(jarvis.input("Enter a model to delete: "))
        delete_model(jarvis, s, answer)

def delete_model(jarvis, s, n):
    with open("saved_models.txt", 'r') as file_read:
        lines = file_read.readlines()
        counter = 0
        with open("saved_models.txt", 'w') as file_write:
            for line in lines:
                if counter is not n:
                    file_write.write(line)
                counter +=1
    jarvis.say("Here is the updated list")
    print("\n")
    view_saved_models(jarvis, s)
