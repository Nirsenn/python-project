import re
from scipy.sparse import csr_matrix
import math #calcul du logarithme pour la matrice IDF
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import Counter
from scipy.sparse import csr_matrix

class SearchEngine:

    def __init__(self, corpus):
        self.corpus = corpus
        self.id2doc = corpus.id2doc
        self.ndoc = corpus.ndoc

        # 1. Construire vocabulaire 
        self.vocab = corpus.freq_mots()[0]

        # 2. Construire Matrice TF
        self.mat_TF = self.matriceTF(self.vocab)

        # 3. Calcul IDF
        self.idf = self.IDF(self.vocab)

        # 4. Matrice TF-IDF
        self.mat_TFxIDF = self.matriceTF_IDF()

    # MATRICE TF
    def matriceTF(self, vocab):
        mots = list(vocab.keys())
        mot2id = {m: i for i, m in enumerate(mots)}
        rows = []
        cols = []
        valeur = []

        for doc_id, doc in self.id2doc.items():
            doc_texte = doc.texte.lower().split()
            counter = Counter(doc_texte)
            for mot, freq in counter.items():
                if mot in mot2id:
                    rows.append(doc_id-1)          # ligne = document (doc_id commence à 1)
                    cols.append(mot2id[mot])       # colonne = mot
                    valeur.append(freq)            # valeur = fréquence

        return csr_matrix((valeur, (rows, cols)), shape=(self.ndoc, len(mots)))

    # VECTEUR IDF
    def IDF(self, vocab):                                                   # Vecteur Inverse Document Frequency
        dIDF = []
        for mot in vocab:
            dIDF.append(math.log(self.ndoc / vocab[mot]["docFreq"], 2))     # Calucl de l'idf = log(nb Docs dans le corpus / DocFreq du mot)
        return dIDF

    # MATRICE TF-IDF
    def matriceTF_IDF(self):                                                    # Matrice TF x IDF pour le Corpus
        idfV = np.array(self.idf)                                                
        mat_TFxIDF = self.mat_TF.multiply(idfV)                                  # Multiplication TF * IDF
        mat_TFxIDF = csr_matrix(mat_TFxIDF)                                     # Reconversion en matrice CSR car multiply() change le format
        return mat_TFxIDF


    # VECTEUR TF-IDF POUR LA REQUÊTE
    def mTFxIDFRequete(self, motsCle):                                      # Matrice TF x IDF pour la requête utilisateur
        mTF = [[]]
        mots = list(self.vocab.keys())                                      # Liste des mots
        for j in range(len(mots)):                                          # Pour chaque mot
            mTF[0].append(motsCle.count(mots[j]))                           # Compte le nb d'occurences du mot du vocabulaire parmis les mots clés de la requête
        mat_TFR = csr_matrix(mTF)                                           # Matrice TFR
        idfrV = np.array(self.idf)
        mat_TFRxIDFR = mat_TFR.multiply(idfrV)                              # Multiplication TF * IDF

        return mat_TFRxIDFR


    # MOTEUR DE RECHERCHE
    def moteurRecherche(self, requete, n=5):
        #Recherche des documents les plus pertinents pour la requête donnée, avec affichage de la progression à chaque étape grâce à tqdm.
        
        # Nettoyage de la requête
        motsCle = self.corpus.nettoyer_texte(requete).split()
        if not motsCle:
            print("La requête est vide après nettoyage.")
            return pd.DataFrame()

        # TF-IDF du corpus et de la requête
        print("Calcul des similarités...")
        tfidf = self.mat_TFxIDF
        reqVec = self.mTFxIDFRequete(motsCle).toarray().ravel()
        prodScalaire = tfidf.dot(reqVec)

        # Calcul des scores avec barre de progression
        normetfidf = np.linalg.norm(tfidf.toarray(), axis=1)
        normetfidfr = np.linalg.norm(reqVec)
        cosinus = prodScalaire / (normetfidf * normetfidfr + 1e-10)

        # Filtrage des documents pertinents
        print(f"Filtrage des {n} documents pertinents...")
        topN = np.argsort(cosinus)[::-1][:n]

        # Construction du DataFrame des résultats
        print(f"Construction du DataFrame des {len(topN)} meilleurs documents...")
        data = []
        doc_ids = list(self.id2doc.keys())
        for i in tqdm(topN, desc="Construction DataFrame"):
            doc = self.id2doc[doc_ids[i]]
            data.append({
                "id": doc_ids[i],
                "titre": doc.titre,
                "date": doc.date,
                "score": cosinus[i],
                "texte": doc.texte[:200] + "..." if len(doc.texte) > 200 else doc.texte,
                "type": doc.type
            })

        return pd.DataFrame(data)
    
    def moteurRechercheFiltre(self, requete, ids_docs, n=5):
        # Recherche sur tout le corpus
        resultat = self.moteurRecherche(requete, n=len(self.id2doc))

        if resultat.empty:
            return resultat  # Rien trouvé

        # Filtrer par id
        resultat = resultat[resultat["id"].isin(ids_docs)]

        # Reprendre les n meilleurs
        return resultat.head(n)

    
    # Bout de code pour faire la recherche
    def recherche(self):
        recherche = True
        print("Tappez 'stop' pour terminer la recherche...")                
        while recherche:
            requete = (str(input("Entrez un ou plusieurs mots clés : ")))
            if requete == "stop":
                recherche = False
            elif requete =="":
                print("Veuillez entrer un mot.")
            else:
                df = self.moteurRecherche(requete)
                print(df)
