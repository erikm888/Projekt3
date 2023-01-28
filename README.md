# Web Scrapper
Tento program je navrhnutý tak, aby vytvořil soubor csv, který obsahuje štatistiky výsledků českého hlasování. Program potřebuje dva argumenty:

- link na územní celek, který chceme scrappovať. Link je zo stránky https://www.volby.cz/
- jméno výstupního souboru s .csv príponou

## Príklad argumentov
python scrapper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" example.csv

## Požadavky
1. Vytvoriť si vlastné virtuálni prostredí pomocou príkazu python -m venv. Detailný návod k dispozícii zde https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
2. Spustiť virtuálne prostredie pomocou source env/bin/activate
3. Soubor requirements.txt obsahuje všechny potrebné knihovny ke spuštění kódu. Dajú sa nainstalovať pomocí pip install -r requirements.txt
