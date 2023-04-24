import bs4
import urllib.request


def stl_finder(query):
    # jarvis.say("Would you like to search for a model or view saved models\n")
    # query = jarvis.input("(search/saved): ")
    if query == "search":
        return "search"
    elif query == "saved":
        return "view_saved_models"

def get_models(url):
    try:
        response = urllib.request.urlopen(url)
    except Exception as e:
        return []
    doc = bs4.BeautifulSoup(response, features="lxml")
    
    list_view = doc.find("div", class_ = "list-view")
    results = list_view.find("div", class_ = "")
    links = results.find_all("div", class_ = "SearchResult_ListView-0-2-229")
    models = []
    for link in links:
        href = link.find_all("a")[0]["href"]
        if href[0:4] == "http":
            models.append(href)
    return models

def save_model(i, first, file):
    models = ["model1", "model2", "model3"]
    if i < 0 or i > len(models):
        # jarvis.say("Invalid model number")
        invalid = True
        while(invalid):
            i = 1
            if i > 0 and i < len(models):
                invalid = False
    if first:
        return True
        
    with open(file, "a") as file:
        return True

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
    # view_saved_models(jarvis, s)  # Re-displays the list of saved models