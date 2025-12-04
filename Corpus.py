import pandas as pd
from Document import Document
from Author import Author
from datetime import datetime
import re
from collections import Counter
import numpy as np
from scipy.sparse import csr_matrix
import math #calcul du logarithme pour la matrice IDF

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
        self.naut = len(self.authors)
    
    def add_document(self, doc_id, doc):
        #document = Document(titre, auteur, date, url, texte) #ne pas créer un document mais prendre un objet document directement en entrée?
        self.id2doc[doc_id] = doc
        if self.id2doc[doc_id].auteur not in self.authors.keys():
            self.authors[self.id2doc[doc_id].auteur] = Author(self.id2doc[doc_id].auteur).add(doc_id, doc)
    

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
                'type' : doc.type
            })
        return pd.DataFrame(data)

    def save(self, filename):
        df = self.to_dataframe()
        df.to_csv(filename, index=False)

    def load(self, filename):
        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            doc = Document(row['titre'], row['auteur'], datetime.strptime(row['date'], "%Y-%m-%d"), row['url'], row['texte'])
            self.add_document(row['id'], doc)
        return self
    
    def search(self, texte, mot):
        c = 1
        regex = r"\b" + mot + r"\b"                                                             #pattern du mot à trouver
        passages = re.finditer(regex, texte)
        for passage in passages:                                                                #pour chaque passage trouvé
            debut = passage.start() - 30                                                        #on prend un extrait de texte débutant 30 caractères avant et finissant 30 caracères après le mot
            fin = passage.end() + 30
            if debut < 0:                                                                       #si l'indice de début est négatif on le remet à 0
                debut = 0
            if fin >= len(texte):                                                               #si l'indice de fin est plus grand que la chaine, on le met à la fin de celle ci
                fin = len(texte) - 1
            print(c, ":", texte[debut:fin])                                                     #affichage de chaque passage correspondant
            c+=1
        return c
    
    def concorde(self, texte, mot, taille):
        i = 0
        regex = r"\b" + mot + r"\b"                                                             #pattern à trouver (le mot en paramètre exclusivement)
        passages = re.finditer(regex, texte)                                                    #stocker les indices de toutes les occurences du mot dans le texte
        df = pd.DataFrame(columns=["contexte gauche", "motif trouvé", "contexte droit"])        #création du Dataframe
        for passage in passages:                                                                #Pour chaque occurence du mot...
            strt = "..."
            end = "..."
            debut = [(passage.start() - taille), (passage.start()-1)]                           #le contexte gauche commence taille caractères avant le début du mot et se termine 1 caractère avant
            fin = [(passage.end() + 1), (passage.end() + taille)]                               #le contexte droit commence 1 caractère après la fin du mot et se termine taille caractères après
            if debut[0] < 0:                                                                    #si l'indice du contexte gauche est plus petit que 0 (sors de la chaine) ont le met à 0
                debut[0] = 0                                                                   
                strt = ""                                                                        #et on ne met pas de "..." car il n'y a rien avant
            if debut[1] < 0:
                debut[1] = 0
                strt = ""
            if fin[1] >= len(texte):                                                            #si l'indice de din du contexte droit est plus grand que la taille de la chaine alors il se termine à la fin de celle ci
                fin[1] = len(texte) - 1
                end = ""                                                                        #et on ne met pas de "..." car il n'y a rien après
            if fin[0] >= len(texte):
                fin[1] = len(texte) - 1
                end = ""
            gauche = strt + texte[debut[0]:debut[1]]   
            droite = texte[fin[0]:fin[1]] + end
            df.loc[i] = pd.Series({"contexte gauche" : gauche, "motif trouvé": mot, "contexte droit": droite})  #ajout de la ligne dans le dataframe
            i+=1
        pd.set_option('display.width', 200)                                                     #paramètre pour que la dataframe s'affiche sur toute la longeur du terminal lors du print
        print(df)


    def nettoyer_texte(self, texte):

        texte = texte.lower()                       # Mise en minuscules

        texte = texte.replace("\n", " ")            # Suppression des retours ligne

        texte = re.sub(r"[^\w\s]", " ", texte)      # Suppression de la ponctuation tout sauf lettres/chiffres/underscore/espaces
        
        texte = re.sub(r"\d+", " ", texte)          # Suppression de la ponctuation des chiffres 

        texte = re.sub(r"\s+", " ", texte).strip()   # Suppression des espaces multiples

        return texte


    def stats(self, n=10):
        data = self.freq_mots(n)                               # Récupère le vocabulaire du Corpus et les données sous forme de Dataframe
        print("Nombre de mots différents :", len(data[0]))     # Nombre de mots différents = longueur du vocabulaire
        print(f"Les {n} mots les plus fréquents :")
        print(data[1].head(n))                                 # Affichage des n premiers éléments du dataframe trié


    def freq_mots(self, n=10):
        mot_id = 1
        vocabulaire = {}                                        # Dictionnaire de forme {mot : {id : x, occurrences : y, docFreq : z}}
        motsDoc = []                                            # Liste des mots uniques pour chaque document

        for doc in self.id2doc.values():                            # Boucle sur tous les documents du corpus
            texte = self.nettoyer_texte(doc.texte)                  # Nettoie le texte
            mots = re.split(r"[ \t\n,;.:!?()\"']", texte)             # Découpe le texte avec plusieurs délimiteurs
            for mot in mots:
                mot = mot.strip()                                      # Supprime les espaces au début et à la fin du mot
                if mot!= "":
                    if mot in vocabulaire:
                        vocabulaire[mot]["occurences"] += 1         # Incrémenter le nombre d'occurences
                    else:
                        vocabulaire[mot] = {}                    # Le mot est intègré au vocabulaire
                        vocabulaire[mot]["id"] = mot_id
                        mot_id += 1
                        vocabulaire[mot]["occurences"] = 1
            motsDoc.append(set(mots))                           # Stocke les mots uniques du document
        
        v = vocabulaire.values()                                # Données du vocabulaire
        occu = [item['occurences'] for item in v]                # Tableau des occurences
        freq = pd.DataFrame({'mot': list(vocabulaire.keys()), 'term frequency' : occu})      # Transformer en DataFrame
        
        docFreq = pd.Series([mot for s in motsDoc for mot in s]).value_counts()         # Ajout de la colonne Document Frequency
        freq["document frequency"] = freq["mot"].apply(lambda m: docFreq.get(m, 0))

        freq = freq.sort_values(by='term frequency', ascending=False).reset_index(drop=True)    # Tri du Dataframe par ordre croissant des occurences

        for mot in vocabulaire.keys():
            vocabulaire[mot]["docFreq"] = docFreq.get(mot, 0)                                  # Ajout de docFreq dans le dictionnaire vocabulaire

        return [vocabulaire, freq]                                              # Renvoie le vocabulaire ET le datarframe
