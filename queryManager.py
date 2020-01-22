# Classe contente i metodi per settare le query in sparql e ottenere le info dei quadri

from SPARQLWrapper import SPARQLWrapper, JSON


class QueryManager:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    def __init__(self, painting):
        self.painting = painting

        print("Effettuo query per il quadro " + painting)

    def setQuery(self, query):
        self.sparql.setQuery(query)

        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        return results

    def getName(self):
        query = """
            SELECT ?nome
            WHERE {
              ?quadro wdt:P31 wd:Q3305213 .
              ?quadro rdfs:label ?nome FILTER regex(?nome, "%s") .
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            } LIMIT 1 
        """ % self.painting

        results = self.setQuery(query)

        for result in results["results"]["bindings"]:
            name = result["nome"]["value"]
        print("Il nome del quadro e' " + name)

        return name

    def getAuthor(self):
        query = """
            SELECT ?autore
            WHERE {
              ?quadro wdt:P31 wd:Q3305213 .
              ?quadro rdfs:label ?nome FILTER regex(?nome, "%s") .
              ?quadro wdt:P170 ?a .
              ?a rdfs:label ?autore .
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            } LIMIT 1 
        """ % self.painting

        results = self.setQuery(query)

        for result in results["results"]["bindings"]:
            author = result["autore"]["value"]
        print("Il nome dell'autore del quadro e' " + author)

        return author

    def getDate(self):
        query = """
            SELECT ?data
            WHERE {
              ?quadro wdt:P31 wd:Q3305213 .
              ?quadro rdfs:label ?nome FILTER regex(?nome, "%s") .
              ?quadro wdt:P571 ?data .
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            } LIMIT 1 
        """ % self.painting

        results = self.setQuery(query)

        for result in results["results"]["bindings"]:
            date = result["data"]["value"]
        print("Il quadro risale al " + date)

        return date

    # datetime.strptime(result["data"]["value"], "%Y-%m-%dT%H:%M:%SZ").strftime('%d-%m-%Y')

    def getMuseum(self):
        query = """
            SELECT ?museo
            WHERE {
              ?quadro wdt:P31 wd:Q3305213 .
              ?quadro rdfs:label ?nome FILTER regex(?nome, "%s") .
              ?quadro wdt:P276 ?m .
              ?m rdfs:label ?museo .
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            } LIMIT 1 
        """ % self.painting

        results = self.setQuery(query)

        for result in results["results"]["bindings"]:
            museum = result["museo"]["value"]
        print("IL quadro e' esposto al museo " + museum)

        return museum
