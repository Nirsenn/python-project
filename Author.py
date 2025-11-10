from Document import Document

class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {}

    def add(self, doc_id, document):
        self.production[doc_id] = document
        self.ndoc = len(self.production)

    def __str__(self):
        return f"Auteur : {self.name} - {self.ndoc} documents" 

    def __repr__(self):
        return f"Auteur : (name = '{self.name}') - (Nombre = '{self.ndoc}') documents" 
    
    def get_taille_moyenne_documents(self):
        if self.ndoc == 0:
            return 0
        total_caracteres = sum(len(doc) for doc in self.production.values())
        return f"Nombre de documents produits : {self.ndoc} - Taille moyenne des documents : {total_caracteres // self.ndoc} caractères"
