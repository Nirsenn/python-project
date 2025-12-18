import pandas as pd
from Document import Document, RedditDocument, ArxivDocument
from Author import Author
from datetime import datetime
import re

# Definition du singleton
def singleton(cls):
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    return wrapper


#@singleton   #(Decorateur)
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
            row = {
                'id' : doc_id,
                'titre' : doc.titre,
                'auteur' : doc.auteur,
                'date' : doc.date,
                'url' : doc.url,
                'texte' : doc.texte,
                'taille_texte' : len(doc.texte),
                'type' : doc.type
            }

            if isinstance(doc, RedditDocument):
                row['nb_comment'] = doc.nb_comment
            elif isinstance(doc, ArxivDocument):
                row['coAuteur'] = doc.coAuteur
            data.append(row)

        return pd.DataFrame(data)

    # Sauvegarde du Corpus au format csv
    def save(self, filename):
        df = self.to_dataframe()
        df.to_csv(filename, index=False, sep="\t", encoding="utf-8")

    # Charger un document csv en objet corpus
    def load(self, filename):
        df = pd.read_csv(filename, sep="\t")
        for _, row in df.iterrows():
            doc = Document(row['titre'], row['auteur'], datetime.strptime(row['date'], "%Y-%m-%d"), row['url'], row['texte'])
            self.add_document(row['id'], doc)
        return self
    
    # Affiche le passage d'un mot dans les textes
    def search(self, texte, mot):
        c = 1
        regex = r"\b" + re.escape(mot) + r"\b"                                                             #pattern du mot à trouver
        for passage in re.finditer(regex, texte):                                                                #pour chaque passage trouvé
            debut = max(passage.start() - 30, 0)                                                       #on prend un extrait de texte débutant 30 caractères avant et finissant 30 caracères après le mot
            fin = min(passage.end() + 30, len(texte))
            print(c, ":", texte[debut:fin])                                                     #affichage de chaque passage correspondant
            c += 1
        return c
    
    # Affiche le passage d'un mot dans les textes sous forme de dataframe
    def concorde(self, texte, mot, taille):
        regex = r"\b" + re.escape(mot) + r"\b"                                                             #pattern à trouver (le mot en paramètre exclusivement)
        passages = []                                                   #stocker les indices de toutes les occurences du mot dans le texte
        for passage in re.finditer(regex, texte):                                                                #Pour chaque occurence du mot...
            debut = max(passage.start() - taille, 0)                        #le contexte gauche commence taille caractères avant le début du mot et se termine 1 caractère avant
            fin = min(passage.end() + taille, len(texte))                              #le contexte droit commence 1 caractère après la fin du mot et se termine taille caractères après
            gauche = texte[debut:passage.start()]  
            if debut > 0:   # si on n’est pas au tout début
                gauche = "..." + gauche
            droite = texte[passage.end():fin] # contexte droit
            if fin < len(texte):   # si on n’est pas à la toute fin
                droite = droite + "..."
            passages.append([gauche, passage.group(), droite])
        df = pd.DataFrame(passages, columns=["contexte gauche", "motif trouvé", "contexte droit"])        #création du Dataframe
        print(df)

    # Nettoie le texte pour le rendre exploitable
    def nettoyer_texte(self, texte):
        texte = texte.lower()                       # Mise en minuscules
        texte = texte.replace("\n", " ")            # Suppression des retours ligne
        texte = re.sub(r"[^\w\s]", " ", texte)      # Suppression de la ponctuation tout sauf lettres/chiffres/underscore/espaces
        texte = re.sub(r"\d+", " ", texte)          # Suppression de la ponctuation des chiffres 
        texte = re.sub(r"\s+", " ", texte).strip()   # Suppression des espaces multiples
        return texte

    # Affiche les mots les plus fréquents
    def stats(self, n=10):
        data = self.freq_mots(n)                               # Récupère le vocabulaire du Corpus et les données sous forme de Dataframe
        print("Nombre de mots différents :", len(data[0]))     # Nombre de mots différents = longueur du vocabulaire
        print(f"Les {n} mots les plus fréquents :")
        print(data[1].head(n))                                 # Affichage des n premiers éléments du dataframe trié

    # Compte la fréquence de tous les mots dans le corpus, par terme puis par documents
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
