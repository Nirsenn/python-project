# Projet Python – Analyse et recherche de documents (Reddit & ArXiv)

**Auteurs :** Aissatou Lamarana Barry & Nissrine Ben Ayou  
**Année universitaire :** 2025–2026  
**Enseignant :** Tetiana Yemelianenko  
**UE :** Programmation de Spécialité – Python  

---

##  Description

Ce projet a pour objectif de construire un **corpus de documents** à partir de différentes sources (Reddit, ArXiv), puis de permettre leur **analyse textuelle**, leur **indexation** et leur **recherche** à l’aide de techniques de traitement automatique du langage naturel (NLP).

Le projet s’inscrit dans le cadre des **TDs de Programmation de Spécialité (Python)** et vise à mettre en pratique :

* la programmation orientée objet,
* la manipulation de données textuelles,
* l’analyse de corpus,
* la conception d’un moteur de recherche simple.

Le projet utilise notamment :

* l’API Reddit via `praw`
* des flux ArXiv (XML)
* des structures de corpus et documents personnalisées
* des outils de NLP (NLTK, TF, TF-IDF, matrices creuses, etc.)

---

## Objectifs

* Collecter des documents depuis différentes sources : CSV, API, web scraping.
* Structurer les documents et les auteurs pour faciliter l’analyse.
* Nettoyer et prétraiter les textes (ponctuation, chiffres, casse).
* Construire un corpus et effectuer des analyses textuelles (statistiques, concordancier).
* Implémenter un moteur de recherche par mots-clés avec scores **TF** et **TF-IDF**.
* Créer une interface interactive dans **Jupyter Notebook** pour la recherche, la visualisation et la comparaison des corpus.
* Observer l’évolution temporelle des mots et générer des **Word Clouds**.

---

## TDs et fonctionnalités

### TD3 – Extraction et prétraitement des données

* Collecte de données via fichiers CSV, API externes et web scraping (Reddit, ArXiv).
* Découpage des textes en phrases ou mots.
* Construction du vocabulaire du corpus et premières statistiques.

### TD4 – Structuration des documents

* Classes `Document` et `Author` pour représenter les textes et leurs auteurs.
* Classe `Corpus` pour regrouper, trier et explorer les documents.
* Autres classes disponibles dans le projet.

### TD5 – Héritage et polymorphisme

* Gestion de documents spécialisés (`RedditDocument`, `ArxivDocument`).
* Utilisation du polymorphisme pour une manipulation uniforme des documents.

### TD6 – Analyse textuelle

* Recherche de mots-clés via **expressions régulières**.
* Construction d’un **concordancier** pour visualiser le contexte des mots.
* Statistiques textuelles : fréquences et comptages.

### TD7 – Moteur de recherche

* Construction d’une **matrice Documents × Termes**.
* Calcul des scores **TF** et **TF-IDF**.
* Recherche par requête avec mesure de similarité (produit scalaire ou cosinus).
* Résultats affichés sous forme de **DataFrame**.

### TD8 – Interface Jupyter Notebook

* Découpage des textes longs en phrases.
* Recherche interactive avec filtres (auteur, type de document, année).
* Interface dynamique avec `ipywidgets`.

### TD9 & TD10 – Interface avancée et exploration comparative

* Comparaison de corpus (Reddit vs ArXiv).
* Analyse des mots spécifiques ou communs.
* Visualisation de l’évolution temporelle des mots.
* Génération de **Word Clouds** interactifs.

---

## Fonctionnalités principales

* Collecte de données : CSV, API, web scraping.
* Gestion et exploration de documents et auteurs.
* Nettoyage et prétraitement textuel.
* Analyse textuelle avancée (TF, TF-IDF, concordancier).
* Moteur de recherche interactif avec filtres.
* Comparaison et visualisation de plusieurs corpus.
* Analyse temporelle des mots et Word Clouds.
* Interface Jupyter Notebook conviviale et modulaire.

---

## Gestion des versions (Git)

Le projet a été versionné avec **Git** dès le début du développement.
Trois **tags** ont été créés afin de marquer les étapes clés du projet :

* **v1** : (TD3-TD5) première version fonctionnelle (bases de la collecte et structuration des documents)
* **v2** : (TD3-TD7) version intermédiaire avec enrichissement des analyses textuelles et du moteur de recherche
* **v3** : (TD3-TD10) **version finale** du projet, correspondant à l’état actuel du dépôt

La présente version du projet correspond donc à la **version finale (v3)**.

---

## Prérequis

* **Python 3.9 ou plus**
* `pip` installé
* Connexion Internet (API Reddit, ArXiv, ressources NLTK)

---

## Installation

### 1 - Cloner ou récupérer le projet

```bash
git clone <https://github.com/Nirsenn/python-project>
cd python-project
```

Ou dézipper l’archive du projet et se placer dans le dossier.

---

### 2 -  Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Ressources NLTK

Lors de la **première exécution**, le projet télécharge automatiquement :

* `punkt_tab`
* `stopwords`

NB: Une connexion Internet est nécessaire la première fois.

---

## Lancer le projet

* Via **un environnenment de developpement integré (IDE) VS Code par exemple** :

Puis ouvrir le notebook principal du projet:

`UserInterface.ipynb` et  executer le premier bloc de code pour lancer l'interface via le notebook.

---

## Interface interactive

Aperçu de l’interface Jupyter Notebook permettant l’exploration et la recherche dans le corpus :

![Interface Jupyter Notebook](images/Interface.png)

---

## Organisation du projet

```
├── api_corpus.py
├── Author.py
├── Document.py
├── Corpus.py
├── data.csv
├── DocumentFactory.py
├── SearchEngine.py
├── interface.py
├── UserInterface.ipynb
├── requirements.txt
└── README.md
```

---

## Bibliothèques utilisées

* praw
* requests
* xmltodict
* python-dateutil
* pandas
* matplotlib
* nltk
* scipy
* numpy
* tqdm

---

## Lien vers le rapport

```bash
https://docs.google.com/document/d/1hgUCek0he4WxjKjYceFKAqiJ4tZ-Qe0lW4a-XYOyQnE/edit?usp=sharing

```

---

## Licence

Projet à usage pédagogique.
