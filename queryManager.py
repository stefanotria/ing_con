# Classe contente i metodi per settare le query in sparql e ottenere le info dei quadri
from SPARQLWrapper import SPARQLWrapper, JSON


class Query:
    wd = SPARQLWrapper("https://query.wikidata.org/sparql")
    db = SPARQLWrapper("http://dbpedia.org/sparql")
    paint = ""

    def __init__(self, paint):
        self.paint = paint
        self.query = ""
        self.select = ""
        self.where = """?Paint wdt:P31 wd:Q3305213 .\n
                     ?Paint rdfs:label ?Name FILTER regex(?Name, '""" + paint + """' ) ."""

    # restituisce il nome dell'autore del dipinto
    def getAuthor(self):
        self.select += "?Author "
        self.where += """?Paint wdt:P170 ?a .
              ?a rdfs:label ?Author ."""

    # restituisce la data in cui é stata realizzata l'opera
    def getDate(self):
        self.select += "?Date "
        self.where += "?Paint wdt:P571 ?Date . \n"

    # restituisce il nome del museo in cui é custodita l'opera
    def getMuseum(self):
        self.select += "?Museum "
        self.where += """?Paint wdt:P276 ?m .
              ?m rdfs:label ?Museum .\n"""

    # restituisce il movimento del dipinto
    def getMovement(self):
        self.select += "?Movement "
        self.where += """?Paint wdt:P135  ?mov .
                        ?mov rdfs:label ?Movement .\n"""

    # restituisce il genere del dipinto
    def getGenre(self):
        self.select += "?Genre"
        self.where += """?Paint wdt:P136 ?gen .
                        ?gen rdfs:label ?Genre .\n"""

    # restituisce altezza e larghezza del dipinto
    def getDimension(self):
        self.select += "?Height ?Width"
        self.where += """?Paint wdt:P2048  ?Height .
                        ?Paint wdt:P2049 ?Width .\n"""

    def buildUp(self):
        self.query = "SELECT " + self.select
        self.query += "\nWHERE {\n" + self.where + "\nSERVICE wikibase:label { bd:serviceParam wikibase:language 'en'. }\n"
        self.query += "} LIMIT 1 "

    def getInfo(self):
        query = """ 
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?Description {
                ?opera a dbo:Artwork .
                ?opera rdfs:label ?Name FILTER regex(?Name, '""" + self.paint + """') FILTER (lang(?Name) = "en")
                ?opera dbo:abstract ?Description FILTER (lang(?Name) = "en") .
                } LIMIT 1"""
        results = self.setQuery(query, self.db)
        response = {}
        for result in results["results"]["bindings"]:
            for value in results["head"]["vars"]:
                response[value] = result[value]["value"]
        print(response)
        return response

    def setQuery(self, query, wrapper):
        wrapper.setQuery(query)

        wrapper.setReturnFormat(JSON)
        results = wrapper.query().convert()
        return results

    def runQuery(self):
        print(self.query)
        results = self.setQuery(self.query, self.wd)
        response = {}
        for result in results["results"]["bindings"]:
            for value in results["head"]["vars"]:
                response[value] = result[value]["value"]
        print(response)
        return response