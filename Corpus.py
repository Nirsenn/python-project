import pandas as pd
from Document import Document
from Author import Author

# Definition du singleton
def singleton(cls):
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    return wrapper


@singleton   #(Decorateur)
class Corpus:
    def __init__(self, nom, id2aut, id2doc):
        self.nom = nom
        self.authors = id2aut
        self.id2doc = id2doc
        self.ndoc = len(id2doc)
        self.naut = len(id2aut)
    
    def add_document(self, doc_id, titre, auteur, date, url, texte):
        document = Document(titre, auteur, date, url, texte)
        self.id2doc = document
        self.ndoc += 1
        if auteur not in self.authors.keys():
            self.authors[auteur] = Author(auteur)
            self.naut += 1
        self.authors[auteur].add(doc_id, document)
    

    def afficher_par_date(self, n):
        docs = sorted(self.id2doc.values(), key=lambda d: d.date, reverse=True)
        print(f"Tri par date :")
        for doc in docs[:n]:
            print(f"- {doc.date} | {doc.titre} ({doc.auteur})")


    def afficher_par_titre(self, n):
        docs = sorted(self.id2doc.values(), key=lambda d: d.titre.lower())
        print(f"Tri par titre")
        for doc in docs[:n]:
            print(f"- {doc.titre} ({doc.auteur}, {doc.date})")

    def __repr__(self):
        return f"Corpus '{self.nom}' : {self.ndoc} documents, {self.naut} auteurs"

        
    def to_dataframe(self):
        data = []
        for doc_id, doc in self.id2doc.items():
            data.append({
                'id' : doc_id,
                'titre' : doc.titre,
                'auteur' : doc.auteur,
                'date' : doc.date,
                'url' : doc.url,
                'texte' : doc.texte,
                'taille_texte' : len(doc.texte),
                'Type' : doc.type
            })
        return pd.DataFrame(data)

    def save(self, filename):
        df = self.to_dataframe()
        df.to_csv(filename, index=False)

    def load(self, filename):
        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            doc = Document(row['titre'], row['auteur'], row['date'], row['url'], row['texte'])
            self.add_document(row['id'], doc)