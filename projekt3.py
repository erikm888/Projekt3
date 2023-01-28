'''
projekt_3.py: tretí projekt do Engeto Online Python Akademie
author: Erik Milošovič
email: erik.milosovic@gmail.com
discord: erik.m#9937
'''

import sys
import csv
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def makeSoup(web):
    return BeautifulSoup(get(web).text, features="html.parser")


def districts(web, writer):
    table, head = [], []
    soup = makeSoup(web)
    districts = soup.find_all("tr")
    for district in districts:
        cell = district.find_all("td")
        if cell and cell[0].text != "-":
            if not head:
                head = header(urljoin(web, cell[2].a["href"]))
                if head:
                    writer.writerow(head)
            code = int(cell[0].text)
            location = cell[1].text
            voters, released, valid, parties = town(
                urljoin(web, cell[2].a["href"]))
            table = [code, location, voters, released, valid]
            table.extend(parties)
            writer.writerow(table)
    return table, head


def town(web):
    voters = extract(web, "sa2")
    published = extract(web, "sa3")
    valid = extract(web, "sa6")
    parties = extract_parties(web)
    return voters, published, valid, parties


def extract(web, header):
    soup = makeSoup(web)
    info = soup.find("td", class_="cislo", headers=header)
    if info:
        info = info.text.replace("\xa0", "")
    else:
        info = 0
        for cell in soup.find_all("td", class_="cislo", headers="s1"):
            info += extract(urljoin(web, cell.a["href"]), header)
    return int(info)


def extract_parties(web):
    soup = makeSoup(web)
    info = soup.find_all("td", class_="cislo", headers="t1sa2 t1sb3")
    info.extend(soup.find_all("td", class_="cislo", headers="t2sa2 t2sb3"))
    if info:
        for i in range(len(info)):
            info[i] = int(info[i].text.replace("\xa0", ""))
    else:
        for cell in soup.find_all("td", class_="cislo", headers="s1"):
            info_temp = extract_parties(urljoin(web, cell.a["href"]))
            if not info:
                info = info_temp
            else:
                for i in range(len(info)):
                    info[i] += info_temp[i]
    return info


def header(web):
    header = ["Code", "Location", "Registered", "Envelopes", "Valid"]
    soup = makeSoup(web)
    names_of_parties = soup.find_all(
        "td", class_="overflow_name", headers="t1sa1 t1sb2")
    names_of_parties.extend(soup.find_all(
        "td", class_="overflow_name", headers="t2sa1 t2sb2"))
    for i in range(len(names_of_parties)):
        names_of_parties[i] = names_of_parties[i].text
    return names_of_parties


if __name__ == "__main__":
    try:
        #web = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
        #outputFile = "test.csv"
        web = sys.argv[1]
        outputFile = sys.argv[2]
        
    except:
        print("Not enough system arguments")
        exit()
    if not web.startswith("http"):
        print("Not an address")
        exit()
    if not outputFile.endswith(".csv"):
        print("Invalid file name")
        exit()

    with open(outputFile, "w", newline="", encoding='utf-8') as ofile:
        writer = csv.writer(ofile)
        table, head = districts(web, writer)
