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


def okresy(web, writer):
    table, head = [], []
    soup = makeSoup(web)
    okresy = soup.find_all("tr")
    for okres in okresy:
        cell = okres.find_all("td")
        if cell and cell[0].text != "-":
            if not head:
                head = header(urljoin(web, cell[2].a["href"]))
                if head:
                    writer.writerow(head)
            code = int(cell[0].text)
            location = cell[1].text
            volici, vydane, platne, strany = obec(
                urljoin(web, cell[2].a["href"]))
            table = [code, location, volici, vydane, platne]
            table.extend(strany)
            writer.writerow(table)
    return table, head


def obec(web):
    volici = extract(web, "sa2")
    vydane = extract(web, "sa3")
    platne = extract(web, "sa6")
    strany = extract_stran(web)
    return volici, vydane, platne, strany


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


def extract_stran(web):
    soup = makeSoup(web)
    info = soup.find_all("td", class_="cislo", headers="t1sa2 t1sb3")
    info.extend(soup.find_all("td", class_="cislo", headers="t2sa2 t2sb3"))
    if info:
        for i in range(len(info)):
            info[i] = int(info[i].text.replace("\xa0", ""))
    else:
        for cell in soup.find_all("td", class_="cislo", headers="s1"):
            info_temp = extract_stran(urljoin(web, cell.a["href"]))
            if not info:
                info = info_temp
            else:
                for i in range(len(info)):
                    info[i] += info_temp[i]
    return info


def header(web):
    header = ["Code", "Location", "Registered", "Envelopes", "Valid"]
    soup = makeSoup(web)
    nazvy_stran = soup.find_all(
        "td", class_="overflow_name", headers="t1sa1 t1sb2")
    nazvy_stran.extend(soup.find_all(
        "td", class_="overflow_name", headers="t2sa1 t2sb2"))
    for i in range(len(nazvy_stran)):
        nazvy_stran[i] = nazvy_stran[i].text
    return header.extend(nazvy_stran)


if __name__ == "__main__":
    try:
        #web = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
        #outputFile = "test.csv"
        web = sys.argv[1]
        outputFile = sys.argv[2]
        
    except IndexError:
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
        table, head = okresy(web, writer)
