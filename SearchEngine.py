import re
import math
import numpy as np
import pandas as pd
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
    
    def matriceTF(self, vocab):                                             # Matrice Term Frequency
        mTF = []
        mots = list(vocab.keys())                                           # Liste de tous les mots du Corpus
        for i in range(1, len(self.id2doc.values())+1):                     # Pour chaque doc (lignes)
            mTF.append([])                                                  # On ajoute une ligne à la matrice
            for j in range(len(mots)):                                      # Pour chaque mot (colonnes)
                mTF[i-1].append(self.id2doc[i].texte.count(mots[j]))        # On ajoute à la matrice le nb d'occurences du mot j dans le document i (i-1 car les id de la classe Document commencent à 1 et pas à 0)
        mat_TF = csr_matrix(mTF)                                            # Conversion en matrice CSR
        return mat_TF

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
        # Nettoyage de la requête
        motsCle = self.corpus.nettoyer_texte(requete).split()

        if not motsCle:
            print("La requête est vide après nettoyage.")
            return pd.DataFrame()

        # TF-IDF de la requête
        mat_TFxIDF = self.mat_TFxIDF                                        # Matrice TF * IDF du corpus
        mat_TFxIDFR = self.mTFxIDFRequete(motsCle)                          # Matrice TF * IDF de la requête
        reqVec = mat_TFxIDFR.toarray().ravel()                              # Transforme idf en vecteur 1D pour les calcul
        score = {}
        for doc in range(mat_TFxIDF.shape[0]):                              # Pour chaque doc
            docVec = mat_TFxIDF[doc].toarray().ravel()                      # Transforme la matrice en vecteur 1D pour les calculs
            prodScalaire = np.dot(docVec, reqVec)                           # Calcul du Produit Scalaire
            normetfidf = np.linalg.norm(docVec)                             # Calcul de la norme pour le corpus
            normetfidfr = np.linalg.norm(reqVec)                            # Calcul de la norme pour la requête
            cosinus = prodScalaire / (normetfidf * normetfidfr + 1e-10)     # Calcul du cosinus + 1e-10 pour eviter la division par Zero 0
            score[doc] = cosinus                                            # Stockage du score de similarité
        
        triScore = [(doc_id, sc) for doc_id, sc in score.items() if sc > 0]           # Filtrer les documents non pertinents

        if not triScore:
            print("Aucun document trouvé pour cette requête.")
            return pd.DataFrame()
        
        triScore = sorted(score.items(), key=lambda x: x[1], reverse=True)  # Tri par ordre décroissant

        # Construire un DataFrame
        data = []
        for doc_id, sc in triScore[:n]:
            doc_ids = list(self.id2doc.keys())
            doc = self.id2doc[doc_ids[doc_id]]
            data.append({
                "id": doc_ids[doc_id], 
                "titre": doc.titre,
                "date": doc.date,
                "score": sc,
                "texte": doc.texte[:200] + "..." if len(doc.texte) > 200 else doc.texte
            })
        return pd.DataFrame(data)
    
    # Bout de code pour faire la recherche

    def recherche(self):
        recherche = True
        print("Tappez 'stop' pour terminer la recherche...")                
        while recherche:
            requete = (str(input("Entrez un mot clé : ")))
            if requete == "stop":
                recherche = False
            elif requete =="":
                print("Veuillez entrer un mot.")
            else:
                df = self.moteurRecherche(requete)
                print(df)
