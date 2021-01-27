# Kamal Chafik
# My first web scrapper with Ville de Montreal

# Read state of 'patinoires' and return open and good condition ones

# imports
from bs4 import BeautifulSoup
import requests

# set variables and open website to take content

siteMTL = "http://ville.montreal.qc.ca/portal/page?_pageid=5798,94909650&_dad=portal&_schema=PORTAL"
siteContent = requests.get(siteMTL).text

siteContentSoup = BeautifulSoup(siteContent, "html.parser")

skatingTable = siteContentSoup.find("table", attrs={"class": "tabDonnees"})

arrondissements = siteContentSoup.find_all('h2', )
cpt = 0
listeMaster = []
listeCondition = []

while True:
    try:
        listeMaster.append(arrondissements[cpt].text)
        i = 0
        tableData = skatingTable.find_all("tr")
        for i in range(len(tableData)):
            for td in tableData[i].find_all("td"):
                listeCondition.append(td.text)
        listeMaster[cpt] = [listeMaster[cpt], listeCondition]
        listeCondition = []
        skatingTable = skatingTable.find_next("table", attrs={"class": "tabDonnees"})
        cpt += 1
    except:
        break

del listeMaster[len(listeMaster) - 1]


def choisirArrondissement() -> int:
    print("Quel arrondissement voulez-vous vérifier ?")
    for i in range(len(listeMaster)):
        print(f"\t{i + 1}- {listeMaster[i][0]}")
    while True:
        choix = int(input("Votre choix : ")) - 1
        if (choix >= 0 and choix < len(listeMaster)):
            return choix


def demanderOuiNon() -> int:
    continuer = -1
    while True:
        try:
            while (continuer < 0 or continuer > 1):
                print("Voulez vous choisir un autre arrondissement ? \n0- Non\n1- Oui")
                continuer = int(input())
            return continuer
        except:
            print("Veuillez entre une valeur ente 0 et 1")
    return -1


choisirEncore = 1
while (choisirEncore == 1):
    choixClavier = choisirArrondissement()
    print(f"\n---------------------------------\nPatinoires ouvertes et en bonne condition à [{listeMaster[choixClavier][0]}]\n\n")

    for i in range(0, len(listeMaster[choixClavier][1]), 6):
        if "PP" in listeMaster[choixClavier][1][i] and "Oui" in listeMaster[choixClavier][1][i + 1] and ("Bon" in listeMaster[choixClavier][1][i + 5] or "Exc" in listeMaster[choixClavier][1][i + 5]):
            print(f"Patinoire: {listeMaster[choixClavier][1][i]} \n\tOuverte: {listeMaster[choixClavier][1][i + 1]} \n\tCondition: {listeMaster[choixClavier][1][i + 5]}\n----------------------------------\n")

    choisirEncore = demanderOuiNon()