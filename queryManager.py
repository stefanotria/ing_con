# Classe contente i metodi per settare le query in sparql e ottenere le info dei quadri
from SPARQLWrapper import SPARQLWrapper, JSON
from urllib.error import HTTPError
import time


class Query:
    wd = SPARQLWrapper("https://query.wikidata.org/sparql")
    db = SPARQLWrapper("http://dbpedia.org/sparql")
    paint = ""

    def __init__(self, paint):
        self.paint = paint
        self.query = ""
        self.select = ""
        self.where = """wd:""" + paint + """ rdfs:label ?Paint ."""
        self.filter = ""

    # restituisce il nome dell'autore del dipinto
    def getAuthor(self):
        self.select += "?Author "
        self.where += """OPTIONAL{wd:""" + self.paint + """ wdt:P170 ?a .}
              OPTIONAL{?a rdfs:label ?Author .}"""
        self.filter += "FILTER(lang(?Author)='en')\n"

    # restituisce la data in cui e' stata realizzata l'opera
    def getDate(self):
        self.select += "?Date "
        self.where += "OPTIONAL{wd:" + self.paint + " wdt:P571 ?Date .} \n"

    # restituisce il nome del museo in cui e' custodita l'opera
    def getMuseum(self):
        self.select += "?Museum "
        self.where += """OPTIONAL{wd:""" + self.paint + """ wdt:P276 ?m .}
              OPTIONAL{?m rdfs:label ?Museum .}\n"""
        self.filter += "FILTER(lang(?Museum)='en')\n"

    # restituisce il movimento del dipinto
    def getMovement(self):
        self.select += "?Movement "
        self.where += """OPTIONAL{wd:""" + self.paint + """ wdt:P135  ?mov .}
                        OPTIONAL{?mov rdfs:label ?Movement .}\n"""
        self.filter += "FILTER(lang(?Movement)='en')\n"

    # restituisce il genere del dipinto
    def getGenre(self):
        self.select += "?Genre"
        self.where += """OPTIONAL{wd:""" + self.paint + """ wdt:P136 ?gen .}
                        OPTIONAL{?gen rdfs:label ?Genre .}\n"""
        self.filter += "FILTER(lang(?Genre)='en')\n"

    # restituisce altezza e larghezza del dipinto
    def getDimension(self):
        self.select += "?Height ?Width"
        self.where += """OPTIONAL{wd:""" + self.paint + """ wdt:P2048  ?Height .}
                        OPTIONAL{wd:""" + self.paint + """ wdt:P2049 ?Width .}\n"""

    # restituisce la nazione
    def getLocation(self):
        query = """ SELECT ?Location
                    WHERE {
                      OPTIONAL{wd:""" + self.paint + """ wdt:P276 ?m .}
                      ?m wdt:P17 ?Location .
                    } LIMIT 1 """
        results = self.setQuery(query, self.wd, 0)
        response = {}
        for result in results["results"]["bindings"]:
            for value in results["head"]["vars"]:
                response[value] = result[value]["value"]
        print(response)
        return response

    def buildUp(self):
        self.query = "SELECT " + self.select
        self.query += "\nWHERE {\n" + self.where + "\n"
        self.query += self.filter
        self.query += "} LIMIT 1 "

    def getInfo(self, name, author):
        query = """ 
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?Description {
        ?opera a dbo:Artwork .
        ?opera dbo:author ?author .
        ?author rdfs:label ?nameAuthor FILTER regex(?nameAuthor, '""" + author + """') FILTER (lang(?nameAuthor) = "en") .
        
        ?opera rdfs:label ?Name FILTER regex(?Name, '""" + name + """') FILTER (lang(?Name) = "en") .
        ?opera dbo:abstract ?Description FILTER (lang(?Description) = "en") .
        } LIMIT 1"""
        results = self.setQuery(query, self.db, 0)
        response = {}
        for result in results["results"]["bindings"]:
            for value in results["head"]["vars"]:
                response[value] = result[value]["value"]
        if response == {}:
            query = """ 
                    PREFIX dbo: <http://dbpedia.org/ontology/>
                    PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
                    SELECT ?Description {
                    ?opera a dbo:Artwork .
                    ?opera dbo:author ?author .

                    ?opera rdfs:label ?Name FILTER regex(?Name, '""" + name + """') FILTER (lang(?Name) = "en") .
                    ?opera dbo:abstract ?Description FILTER (lang(?Description) = "en") .
                    } LIMIT 1"""
            results = self.setQuery(query, self.db, 0)
            for result in results["results"]["bindings"]:
                for value in results["head"]["vars"]:
                    response[value] = result[value]["value"]
        return response

    def createCollection(self, location):
        query = """ 
                SELECT DISTINCT ?Uri ?Paint ?Author ?Museum ?Genre ?Movement ?Content
                WHERE {
                ?Uri wdt:P31 wd:Q3305213 .
                ?Uri rdfs:label ?Paint FILTER(lang(?Paint)='en').
                ?Uri wdt:P170 ?a .
                ?a rdfs:label ?Author .
                ?Uri wdt:P276 ?m .
                ?m wdt:P17 <""" + location + """>.
                ?m rdfs:label ?Museum .
                ?Uri wdt:P136 ?gen .
                ?gen rdfs:label ?Genre .
                ?Uri wdt:P135 ?mov .
                ?mov rdfs:label ?Movement .
                ?Uri wdt:P180 ?c .
                ?c rdfs:label ?Content .
                FILTER(lang(?Content)='it')
                FILTER(lang(?Author)='en')
                FILTER(lang(?Museum)='en')
                FILTER(lang(?Genre)='en')
                FILTER(lang(?Movement)='en')
                }
                LIMIT 1000"""
        results = self.setQuery(query, self.wd, 0)
        response = {}
        r = []

        for result in results["results"]["bindings"]:
            val = []
            for value in results["head"]["vars"]:
                response[value] = result[value]["value"]
                val.append(response[value])
            r.append(val)
        return r

    def getContent(self):
        query = """
                SELECT (group_concat(DISTINCT ?Content;SEPARATOR=" ") as ?Contents)
                WHERE {
                OPTIONAL{wd:""" + self.paint + """ wdt:P180 ?c .}
                OPTIONAL{?c rdfs:label ?Content .}
                FILTER(lang(?Content)='it')
                }
                LIMIT 1"""
        results = self.setQuery(query, self.wd, 0)
        response = {}
        r = []
        for result in results["results"]["bindings"]:
            val = []
            for value in results["head"]["vars"]:
                response[value] = result[value]["value"]
                val.append(response[value])
            r.append(val)
        return r[0]

    def setQuery(self, query, wrapper, count):  # count: conteggio http error 429
        try:
            wrapper.setQuery(query)
            wrapper.setReturnFormat(JSON)
            results = wrapper.query().convert()
            return results
        except HTTPError as e:
            if e.code == 429:
                if count == 4:
                    print("Timeout error. Terminazione programma.")
                    raise SystemExit
                print("Si e' verificato un HTTP Error 429. Riprovo...")
                time.sleep(5);
                return self.setQuery(query, wrapper, count + 1)
            raise SystemExit

    def runQuery(self):
        results = self.setQuery(self.query, self.wd, 0)
        response = {}
        for result in results["results"]["bindings"]:
            for value in results["head"]["vars"]:
                response[value] = result[value]["value"]
        return response
