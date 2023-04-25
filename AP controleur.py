from bs4 import BeautifulSoup
from selenium import webdriver
import json
import os
from pprintpp import pprint

#haal data uit AP
def getData(link, driver):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    
    entiteiten = False
    datatypes = False
    klassen = {}
    typedict = {}
    
    for d in soup.find_all('div', attrs={"class":"region region--no-space-top"}):
        for h2 in d.find_all('h2'):
            if h2.text == "Entiteiten":
                entiteiten = True
        if entiteiten:
            datatypes = False
            for h3 in d.find_all('h3'):
                attributen = {}
                for tr in d.find_all('tr', attrs={"typeof":"rdfs:Property"}):
                    lijst = []
                    for td in tr.find_all('td'):
                        geenLink = True
                        for a in td.find_all('a'):
                            attrlink = {}
                            if a.text[5:10] == "     ":
                                attrlink[a.text[29:]] = a['href']
                            else:
                                attrlink[a.text] = a['href']
                            lijst.append(attrlink)
                            geenLink = False
                        if geenLink:
                            lijst.append(td.text)
                    
                    attributen[list(lijst[0].keys())[0]] = lijst
                if attributen == {}:
                    attributen[h3.text] = [{'bla':'bla'},{'bla':'bla'},'bla','bla','bla']
                klassen[h3.text] = attributen
        
        for h2 in d.find_all('h2'):
            if h2.text == "Datatypes":
                datatypes = True
        if datatypes:
            entiteiten = False
            for h3 in d.find_all('h3'):
                attributen = {}
                for tr in d.find_all('tr', attrs={"typeof":"rdfs:Property"}):
                    lijst = []
                    for td in tr.find_all('td'):
                        geenLink = True
                        for a in td.find_all('a'):
                            attrlink = {}
                            attrlink[a.text] = a['href']
                            lijst.append(attrlink)
                            geenLink = False
                        if geenLink:
                            lijst.append(td.text)
                    
                    attributen[list(lijst[0].keys())[0]] = lijst
                if attributen == {}:
                    attributen[h3.text] = [{'bla':'bla'},{'bla':'bla'},'bla','bla','bla']
                typedict[h3.text] = attributen
        
    
    stanDict = {}
    stanDict["Entiteiten"] = klassen
    stanDict["Datatypes"] = typedict
    return stanDict


#Haal website op
driver = webdriver.Chrome()
#inp = input("Geef de link van het AP: ")
#try:
links = ["https://data.vlaanderen.be/doc/applicatieprofiel/cultureel-erfgoed-object/",
            "https://data.vlaanderen.be/doc/applicatieprofiel/dienst-transactiemodel/",
            "https://data.vlaanderen.be/doc/applicatieprofiel/dossier/",
            "https://data.vlaanderen.be/doc/applicatieprofiel/generieke-terugmeldfaciliteit/",
            "https://data.vlaanderen.be/doc/applicatieprofiel/notificatie-basis/",
            "https://data.vlaanderen.be/doc/applicatieprofiel/mobiliteit/dienstregeling-en-planning/tijdstabellen/"]

data = getData("https://data.vlaanderen.be/doc/applicatieprofiel/doelgericht-digitaal-transformeren/", driver)
pprint(data)
#except:
#    print("Werkt niet!")

