from plugin import plugin
import bs4
import urllib.request
from colorama import Fore


@plugin("stl_finder")
def stl_finder(jarvis, s):
    # Determines whether the user wants to search or view saved
    jarvis.say("Would you like to search for a model or view saved models\n")
    command = jarvis.input("(search/saved): ")
    if command == "search":  # User wants to search
        search(jarvis,s)
    elif command == "saved":  # User wants to see saved models
        view_saved_models(jarvis, s)
    print("\n")
    
def search(jarvis, s):
    # The start and end of the url
    ROOT_URL = "https://thangs.com/search/"
    URL_END = "?scope=all"

    # Gets the terms to search for from the user
    search_term = jarvis.input("What would you like to search for?\n")
    search_term = search_term.replace(" ", "_")

    #Uses the search terms to create the url
    url = ROOT_URL + search_term + URL_END
    models = get_models(url)

    # Prints the first three models
    counter = 0
    if len(models) == 0:
        jarvis.say("No results found")
        return
    jarvis.say("\nResults:")
    for i in range(3):
        counter = print_models(models, counter, jarvis, s)

    # Continues to print while user says "y"
    response_yes = True
    while counter < len(models)-3 and response_yes:
        response = jarvis.input("\nWould you like to see more? (y/n): ")
        if response == 'y':
            for i in range(3):
                counter = print_models(models, counter, jarvis, s)
        else:
            response_yes = False;
    
    # Prompts to save model
    response = jarvis.input("\nWould you like to save a model? (y/n): ")
    if response == 'y':
        model_number = int(jarvis.input("\nWhich model would you like to save: "))
        save_model(jarvis, s, models, model_number)

# Scrapes url and returns a list of models
def get_models(url):
    try:
        response = urllib.request.urlopen(url)
    except Exception as e:
        return []
    
    # Navigates the html of the site
    doc = bs4.BeautifulSoup(response, features="lxml")
    list_view = doc.find("div", class_ = "list-view")
    divs = list_view.find("div", class_ = "")
    links = divs.find_all("div", class_ = "SearchResult_ListView-0-2-229")

    # Saves the models to models
    models = []
    for link in links:
        href = link.find_all("a")[0]["href"]
        if href[0:4] == "http":
            models.append(href)
    return models

# Saves the ith model from models
def save_model(jarvis, s, models, i):
    # Ensures i is a valid index
    if i < 0 or i > len(models):
        jarvis.say("Invalid model number", Fore.RED)
        invalid = True
        while(invalid):
            i = int(jarvis.input("Please enter a new model number: "))
            if i > 0 and i < len(models):
                invalid = False
    
    # Saves the model
    with open("saved_models.txt", "a") as file:
        file.write(f"{models[i-1]}\n")
    jarvis.say(f"\nModel {i} has been saved")

# Outputs the contents of the saved file
def view_saved_models(jarvis, s):
    with open("saved_models.txt", 'r') as file:
        for i, link in enumerate(file):
            jarvis.say(f"({i}) {link}")
    
    # Prompts the user to edit the list
    response = jarvis.input("Would you like to edit the list? (y/n): ")
    if response is "y":
        response = int(jarvis.input("Enter a model to delete: "))
        delete_model(jarvis, s, response)

# Allows the user to delete the nth models from the file
def delete_model(jarvis, s, n):
    with open("saved_models.txt", 'r') as file_read:
        lines = file_read.readlines()
        counter = 0
        # Copies all models besides the nth model
        with open("saved_models.txt", 'w') as file_write:
            for line in lines:
                if counter is not n:
                    file_write.write(line)
                counter +=1
    jarvis.say("Here is the updated list")
    print("\n")
    view_saved_models(jarvis, s)  # Re-displays the list of saved models

# Prints the model with its associated model number
def print_models(models, counter, jarvis, s):
    jarvis.say(f"({str(counter+1)}) {models[counter]}")
    counter += 1
    return counter
