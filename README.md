# Engeto 3 projekt

Třetí projekt na Pzthon akamdemii od Enegeta.

## Popis projektu

Tento projet slouží k extrahování výsledků voleb z roku 2017. Odkaz k prohlédnutí najdete [zde](https://github.com/Pavlick-tech/scraping/blob/main/scraper.py) .

## Instalace knihoven

Knihovny, které jsou použity v kódu, jsou uloženy v sourboru requirements.txt. Pro instalaci doporučujeme použít nové virutální prostředí a s nainstalovaným manažerem spustit následovně:

$ pip3 --version
$ pip3 install -r requirements.txt

## Spuštění projektu
Spuštění souboru scraper.pz v rámci přík. řádky požaduje dva povinné argumenty.

python scraper.py <odkaz-uzemniho-celku> <vysledny-soubor>

Následně se vám stáhnou výsledky ve formátu csv.
  
Částečný výstup:
kod,nazev,voliciVSeznamu,vydaneObalky,platneHlasy,Občanská demokratická strana,........
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
589276,Bílovice-Lutotín,294,178,174,11,0,0,20,0,5,22,1,0,2,0,0,16,0,2,58,0,0,10,0,0,0,1,26,0
589276,Bílovice-Lutotín,137,101,101,2,0,0,12,0,3,18,0,0,2,0,0,14,0,1,25,0,0,12,0,0,0,0,12,0
589284,Biskupice,238,132,131,14,0,0,9,0,5,24,2,1,1,0,0,10,2,0,34,0,0,10,0,0,0,0,19,0
  

