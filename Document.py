from datetime import datetime

class Document:
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = ', '.join([auteur])
        self.date = date.strftime("%Y-%m-%d")
        self.url = url
        self.texte = texte
        self.type = None

    def __str__(self):
        return f"Document : {self.titre}" 
    
    def affichage_info(self):
        print(f"Titre : {self.titre}")
        print(f"Auteur : {self.auteur}")
        print(f"Date : {self.date}")
        print(f"Url : {self.url}")
        print(f"Texte : {self.texte[:100]}...")
    
    def getType(self):
        pass
    
# nb_comment  nombre de commentaires postés par les internautes en reaction au message

class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nb_comment, type):
        super().__init__(titre, auteur, date, url, texte)
        self.nb_comment = nb_comment
        self.type = type

    def __str__(self):
        super().affichage_info()
        return f"Nombre de commentaires :{self.nb_comment}"
    
    def getNb_comment(self):
        return self.nb_comment
    
    def setNb_comment(self, nb_comment):
        self.nb_comment = nb_comment
    
    def getType(self):
        return self.type


class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, coAuteur, type):
        super().__init__(titre, auteur, date, url, texte)
        self.coAuteur = ', '.join(coAuteur)
        self.type = type
    
    def __str__(self):
        super().affichage_info()
        return f"Co-Auteur(s) : {self.coAuteur}"
    
    def get_CoAuteur(self):
        return self.coAuteur
    
    def set_CoAuteur(self, id2aut):
        self.coAuteur = id2aut

    def getType(self):
        return self.type


#document.auteur = 1er auteur
#arxivdocument coauteur = tous les autres auteurs