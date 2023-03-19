import requests
from bs4 import BeautifulSoup

#conducting a request of the stated URL above:
def get_title(url:str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find("h1",{"class":"title-title"}).text
    release_year = soup.find("span",{"class":"item-year"}).text
    print("The title of the show is called: " + title)
    return release_year

def get_genres(url:str):
    genre_set = set()
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    genres = soup.find_all("span",{"class":"item-genres"})
    for x in range(0,len(genres)):
        genre_set.add(genres[x].text.replace(",",""))
    return genre_set

def get_cast(url:str):
    cast_set = set()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    cast = soup.find_all("span",{"class":"item-cast"})
    for x in range(0,len(cast)):
        cast_set.add(cast[x].text.replace(",",""))
    return cast_set

def commonalities(url:str, url_comp:str):
    first_one = get_title(url)
    second_one = get_title(url_comp)
    if(first_one == second_one):
        print("They were both released in: " + first_one)
    else:
        print("They were released in different years")
    common_genres = get_genres(url) & get_genres(url_comp)
    common_cast_mem = get_cast(url) & get_cast(url_comp)

    print("They share the following genres: " + common_genres)
    print("They share the following cast members: " + common_cast_mem)


if __name__ == '__main__':
    continued = True
    while continued:
        link_1 = input("please put in the link of the first netflix show you want to compare: ")
        link_2 = input("please put in the link of the second netflix show you want to compare: ")
        
        commonalities(link_1, link_2)

        option = input("If you would like to continue, please type yes: ")
        if(option.lower() == "yes"):
            print("\n")
            continue
        else:
            print("you didn't say yes! Au revoir~")
            continued = False