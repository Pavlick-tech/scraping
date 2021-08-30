import sys
import validators
import requests
import bs4
import csv
import unicodedata

def Main():
    obce = nacistObce()
    dataObci = []

    print("Načítám data z vybraného URL:", sys.argv[1])

    for obec in obce:
        dataObci.append(nacistDataObci(obec))

    print("Ukládám data do souboru:", sys.argv[2])
    with open(sys.argv[2], "w", newline="", encoding="utf-8-sig") as f:
        if len(obce) > 0:            
            header = ["kod","nazev","voliciVSeznamu","vydaneObalky","platneHlasy"]
            for strana in dataObci[0][0]["kandidujiciStrany"]:
                header.extend(strana)    

        writer = csv.writer(f)
        writer.writerow(header)

        for obec in dataObci:
            for item in obec:    
                # write the data
                l = [item["kod"],item["nazev"],item["voliciVSeznamu"],item["vydaneObalky"],item["platneHlasy"]]

                for s in item["kandidujiciStrany"]:
                    l.append(list(s.values())[0])
                
                writer.writerow(l)

    print("Export hotov.")


def nacistObce():
    hlavniStranka = requests.get(sys.argv[1])
    soup = bs4.BeautifulSoup(hlavniStranka.text, "html.parser")
    vsechnyTabulky = soup.find_all("table")
    obce=[]
    for tabulka in vsechnyTabulky:
        teloTabulky = tabulka.findAll("tr")
        for radekTabulky in teloTabulky[2:]:
            obec = {}
            bunkyRadku = radekTabulky.findAll("td")
            #pokud ma radek obsah
            if  bunkyRadku[0].get_text() != "-":
                obec["kod"] = bunkyRadku[0].find("a").get_text()
                obec["nazev"] = bunkyRadku[1].get_text()
                obec["href"] = bunkyRadku[2].find("a")["href"]
                obce.append(obec)
    return obce

def nacistDataOkrsku(urlObce, obec):
    okrsekDetail = {
        "kod": obec["kod"]
    }
    #nacist stranku obce
    hlavniStranka = requests.get(urlObce)
    #parse html obsah
    soup = bs4.BeautifulSoup(hlavniStranka.text, "html.parser")

    okrsekDetail["nazev"] = obec["nazev"]

    #nacist vsechny tabulky
    vsechnyTabulky = soup.find_all("table")

    #casti radky prvni tabulky
    teloTabulky = vsechnyTabulky[0].find_all("tr")

    if len(obec["vsechnyUrlOrsku"]) < 1:
        #obsah tretiho radku
        bunkyRadku = teloTabulky[2].find_all("td")
         #voliči v seznamu
        okrsekDetail["voliciVSeznamu"] = bunkyRadku[3].get_text().strip()
        #vydané obálky
        okrsekDetail["vydaneObalky"] = bunkyRadku[4].get_text().strip()
        #platné hlasy
        okrsekDetail["platneHlasy"]  = bunkyRadku[7].get_text().strip()
 
    else:
        #obsah druheho radku
        bunkyRadku = teloTabulky[1].find_all("td") 
        #voliči v seznamu
        okrsekDetail["voliciVSeznamu"] = unicodedata.normalize("NFKD", bunkyRadku[0].get_text()).replace(" ","")
        #vydané obálky
        okrsekDetail["vydaneObalky"] = bunkyRadku[1].get_text()
        #platné hlasy
        okrsekDetail["platneHlasy"]  = bunkyRadku[4].get_text()    

    kandidujiciStrany = nacistKandidujiciStrany(vsechnyTabulky)
    okrsekDetail["kandidujiciStrany"] = kandidujiciStrany

    return okrsekDetail

def nacistKandidujiciStrany(vsechnyTabulky):
    
    #kandidující strany
    kandidujiciStrany = []
    for tabulka in vsechnyTabulky[1:len(vsechnyTabulky)-1]:
        teloTabulky = tabulka.find_all_next("tr")
        for radekTabulky in teloTabulky[2:len(teloTabulky)-1]:
            bunkyRadku = radekTabulky.findAll("td")
            strana =  {}  
            if len(bunkyRadku) > 0:   
                strana[bunkyRadku[1].get_text()] = unicodedata.normalize("NFKD", bunkyRadku[2].get_text()).replace(" ","")
                kandidujiciStrany.append(strana)  
    #kandidujiciStranyString = ";".join(kandidujiciStrany) 
    return kandidujiciStrany

def nacistUrlOkrsku(soup):
    vsechnyBunky = soup.find_all("td")
    vsechnyOdkazy = []
    #nacist vsechny url ze vsech bunek
    for odkaz in vsechnyBunky:
        if odkaz.get_text() != "-":
             vsechnyOdkazy.append(odkaz.find("a")["href"])

    return vsechnyOdkazy        

def nacistDataObci(obec):
    dataVsechOrsku = []
    obec["vsechnyUrlOrsku"] = ""
    #Slozit url obce
    urlObce = "https://volby.cz/pls/ps2017nss/" + obec["href"]  
    #nacist stranku obce
    hlavniStranka = requests.get(urlObce)
    #parse html obsah
    soup = bs4.BeautifulSoup(hlavniStranka.text, "html.parser")

    #ma li obec vice okrsku - v url hleda substring "xvyber=7103", pokud podminka plati nacist pocet a url okrsku, pokud ne nacist detail
    subsString = "xvyber"
    
    if subsString not in urlObce:

        vsechnyUrlOrsku = nacistUrlOkrsku(soup)
        obec["vsechnyUrlOrsku"] = vsechnyUrlOrsku  

        for uri in vsechnyUrlOrsku:
            urlOkrsku = "https://volby.cz/pls/ps2017nss/" + uri
            dataOkrsku = nacistDataOkrsku(urlOkrsku,obec)
            dataVsechOrsku.append(dataOkrsku)   
        
    else:
            dataOkrsku = nacistDataOkrsku(urlObce,obec)
            dataVsechOrsku.append(dataOkrsku)

    return dataVsechOrsku        
        
try:    
    if len(sys.argv) < 3:
        raise Exception("Missing some mandatory arguments.")
        
    if not validators.url(sys.argv[1]):
         raise Exception("Entered arugment is not valid URL.")

    Main()
        
except Exception as Error:
        print(Error)

finally:
     sys.exit(1)    
