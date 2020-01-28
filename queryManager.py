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
        self.where = """wd:""" + paint + """ rdfs:label ?Paint ."""
        self.filter = "FILTER(lang(?Paint)='en')\n"

    # restituisce il nome dell'autore del dipinto
    def getAuthor(self):
        self.select += "?Author "
        self.where += """OPTIONAL{wd:""" + self.paint + """ wdt:P170 ?a .}
              OPTIONAL{?a rdfs:label ?Author .}"""
        self.filter += "FILTER(lang(?Author)='en')\n"

    # restituisce la data in cui e' stata realizzata l'opera
    def getDate(self):
        self.select += "?Date "
        self.where += "OPTIONAL{wd:" + self.paint +  " wdt:P571 ?Date .} \n"

    # restituisce il nome del museo in cui e' custodita l'opera
    def getMuseum(self):
        self.select += "?Museum "
        self.where += """OPTIONAL{wd:""" +self.paint + """ wdt:P276 ?m .}
              OPTIONAL{?m rdfs:label ?Museum .}\n"""
        self.filter += "FILTER(lang(?Museum)='en')\n"

    # restituisce il movimento del dipinto
    def getMovement(self):
        self.select += "?Movement "
        self.where += """OPTIONAL{wd:""" +self.paint + """ wdt:P135  ?mov .}
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
        self.where += """OPTIONAL{wd:"""+ self.paint + """ wdt:P2048  ?Height .}
                        OPTIONAL{wd:"""+self.paint+ """ wdt:P2049 ?Width .}\n"""

    def buildUp(self):
        self.query = "SELECT " + self.select
        self.query += "\nWHERE {\n" + self.where + "\n"
        self.query += self.filter
        self.query += "} LIMIT 1 "

    def getInfo(self, name):
        query = """ 
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?Description {
                ?opera a dbo:Artwork .
                ?opera rdfs:label ?Name FILTER regex(?Name, '""" + name + """') FILTER (lang(?Name) = "en")
                ?opera dbo:abstract ?Description FILTER (lang(?Description) = "en") .
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
        results = self.setQuery(self.query, self.wd)
        response = {}
        for result in results["results"]["bindings"]:
            for value in results["head"]["vars"]:
                response[value] = result[value]["value"]
        print(response)
        return response