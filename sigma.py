from time import sleep
import threading
import requests
from bs4 import BeautifulSoup
from subprocess import call
import os
    
class Sigmas:

    def __init__(self, URL):
        self.score = 0
        self.films = []
        self.SIGMA_FILMS = ["tt0144084", "tt7286456","tt0780504","tt0075314","tt0137523",
                            "tt0066921", "tt2872718","tt7984734","tt0468569","tt0110912",
                            "tt0068646", "tt2582802","tt1856101"]
        self.SIGMA_NAMES = {
            "tt0144084":"American Psycho (2000) by Mary Harron",
            "tt7286456":"Joker (2019) by Todd Phillips",
            "tt0780504":"Drive (2011) by Nicolas Winding Refn",
            "tt0075314":"Taxi Driver (1976) by Martin Scorsese",
            "tt0137523":"Fight Club (1999) by David Fincher",
            "tt0066921":"A Clockwork Orange (1971) by Stanley Kubrick",
            "tt2872718":"Nightcrawler (2014) by Dan Gilroy",
            "tt7984734":"The Lighthouse (2019) by Robert Eggers",
            "tt0468569":"The Dark Knight (2008) by Christopher Nolan",
            "tt0110912":"Pulp Fiction (1994) by Quentin Tarantino",
            "tt0068646":"The Godfather (1972) by Francis Ford Coppola",
            "tt2582802":"Whiplash (2014) by Damien Chazelle",
            "tt1856101":"Blade Runner 2049 (2017) by Denis Villeneuve",
            }
        self.URL = URL
    
    def get_films(self):
        films = []
        for i in range(1,1000):
            url = self.URL+f"?page={i}"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find_all("div", class_="lister-item-image ribbonize")
            if not results:
                break
            for r in results:
                href = r.find("a")
                films.append(href["href"][7:-1])
        return films
                
    def get_score(self):
        counter = 0
        other = []
        for film in self.SIGMA_FILMS:
            if film in self.films:
                counter+=1
            else:
                other.append(film)
        return (round(counter/len(self.SIGMA_FILMS)*100,1),other)
    
    def show_films(self):
        self.films = self.get_films()
        self.score, other = self.get_score()
        if other:
            temp = []
            for o in other:
                temp.append(self.SIGMA_NAMES[o])
            rec = "To be even more afraid of women consider watching: \n" +\
                "\n".join(temp)
        else:
            rec = ""
        result = f"You are afraid of women on {self.score}%"
        return [result, rec] if rec else [result]

ans = []

def clear():
    _ = call('clear' if os.name == 'posix' else 'cls',shell = True)

def main():
    clear()
    arg = input("Enter url to imdb watchlist: ")
    clear()
    long_running_thread = threading.Thread(target=sigma, args=(arg,))
    long_running_thread.start()
    print_thread = threading.Thread(target=wait, args=(long_running_thread,))
    print_thread.start()
    long_running_thread.join()
    print_thread.join()
    global ans
    for a in ans:
        print(a)
    input()

def sigma(url):
    sigma = Sigmas(url)
    global ans
    ans.extend(sigma.show_films())

def wait(thread):
    while thread.is_alive():
        for i in range(4):
            print("Waiting"+"."*i)
            sleep(1)
            clear()
    clear()
 
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
