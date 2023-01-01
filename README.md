# Web Scrapper
This scrapper is designed to create a cvs file containing the statistics of the czech voting results.
The program needs two arguments:
- link to an okres, from site https://www.volby.cz/
- name of the .cvs file to write into (create)

## Example for arguments
scrapper.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 example.cvs

## Requirements
requirements.txt contains all the necessary libraries needed to run the code
they can be installed using pip
pip install -r requirements.txt