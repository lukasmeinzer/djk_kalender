from bs4 import BeautifulSoup
import requests


def get_spiele_infos(url: str) -> list[dict]:
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    spiel_urls = [item.get("href") for item in soup.find_all("a", class_="bfv-spieltag-eintrag__match-link")]


    spiele: list[dict] = []
    for url in spiel_urls:
        results = {}
        results["link_zum_spiel"] = url
    
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")
    
        ####################### Datum
        datum = soup.find("div", class_="bfv-matchday-date-time")
        if datum:
            datum = datum.find_all("span")[1]
            datum, uhrzeit = (item.strip().strip("/ ") for item in datum.text.split("\n") if item.strip() != "")
            results["datum"] = datum
            results["uhrzeit"] = uhrzeit
        

        ##########################  Mannschaften
        spiel_body = soup.find("div", class_="bfv-matchdata-result__body")

        team0 = spiel_body.find("div", class_="bfv-matchdata-result__team-name bfv-matchdata-result__team-name--team0")
        if team0:
            team0 = team0.text.strip().replace("/"," ")
            results["team0"] = team0

        team1 = spiel_body.find("div", class_="bfv-matchdata-result__team-name bfv-matchdata-result__team-name--team1")
        if team1:
            team1 = team1.text.strip().replace("/"," ")
            results["team1"] = team1
        
        ############ ADressse
        adresse = soup.find("div", class_="bfv-game-info-entry__text")
        if adresse:
            adresse = adresse.text.strip()
            results["adresse"] = adresse


        spiele.append(results)
    return spiele
