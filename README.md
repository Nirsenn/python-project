# Projet Python – Analyse et recherche de documents (Reddit & ArXiv)

**Auteurs :** Aissatou Lamarana Barry & Nissrine Ben Ayou  
**Année universitaire :** 2025–2026  
**Enseignante :** Tetiana Yemelianenko  
**UE :** Programmation de Spécialité – Python  

## Sommaire
- [Description](#description)
- [Objectifs](#objectifs)
- [Contenu des versions](#contenu-par-versions)
  - [V1](#v1)
  - [V2](#v2)
  - [V3](#v3)
- [Fonctionnalités](#fonctionnalités-principales)
- [Architecture du projet](#organisation-du-projet)
- [Prérequis d'installation](#prérequis)
- [Installation](#installation)
- [Apperçu de l'UI](#interface-interactive)
- [Rapport](#lien-vers-le-rapport)


## Description

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



## Objectifs

* Collecter des documents depuis différentes sources : CSV, API, web scraping.
* Structurer les documents et les auteurs pour faciliter l’analyse.
* Nettoyer et prétraiter les textes (ponctuation, chiffres, casse).
* Construire un corpus et effectuer des analyses textuelles (statistiques, concordancier).
* Implémenter un moteur de recherche par mots-clés avec scores **TF** et **TF-IDF**.
* Créer une interface interactive dans **Jupyter Notebook** pour la recherche, la visualisation et la comparaison des corpus.
* Observer l’évolution temporelle des mots et générer des **Word Clouds**.



## Contenu par versions
Chaque tag représente une version différente du projet comme suit :

### V1
#### TD3 – Extraction et prétraitement des données
- **Collecte de données** via fichiers CSV, API externes et web scraping (ex. Reddit, Arxiv).  
- Découpage des textes en phrases ou mots.  
- Construction d’un vocabulaire du corpus et premières statistiques.  

#### TD4 – Structuration des documents
- Classes `Document` et `Author` pour gérer les textes et les auteurs.  
- Classe `Corpus` pour regrouper les documents, trier et explorer les données.
- Autres Classes, voir projet.

#### TD5 – Héritage et polymorphisme
- Gestion de types spécifiques de documents (`RedditDocument`, `ArxivDocument`).  
- Exploitation du polymorphisme pour manipuler différents documents de manière uniforme.

### V2
Contenu de la V1 plus :
#### TD6 – Analyse textuelle
- Recherche de mots-clés et expressions via **expressions régulières**.  
- Construction d’un **concordancier** pour visualiser le contexte des mots.  
- Statistiques textuelles : comptage des mots, fréquence par document et dans le corpus.  

#### TD7 – Moteur de recherche
- Construction d’une **matrice Documents × Termes**.  
- Calcul des scores **TF** et **TF-IDF**.  
- Recherche par mots-clés avec vecteurs de requête et mesure de similarité (produit scalaire ou cosinus).  
- Résultats présentés sous forme de **DataFrame**.

### V3
Version finale, contenu de la V2 plus :
#### TD8 – Interface Jupyter Notebook
- Découpage des textes longs en phrases.  
- Recherche interactive avec filtres : auteur, type de document, année.  
- Affichage dynamique des résultats avec `widgets` (`Text`, `IntSlider`, `Button`, `Output`).  

#### TD9 et TD10 – Interface avancée et exploration comparative
- Comparaison de deux corpus (Reddit vs Arxiv) : mots spécifiques ou communs.  
- Visualisation de l’évolution temporelle des mots.  
- Génération de **Word Clouds** interactifs.  
- Possibilité de filtrer les recherches par auteur, type de document ou période.

## Fonctionnalités principales

* Collecte de données : CSV, API, web scraping.
* Gestion et exploration de documents et auteurs.
* Nettoyage et prétraitement textuel.
* Analyse textuelle avancée (TF, TF-IDF, concordancier).
* Moteur de recherche interactif avec filtres.
* Comparaison et visualisation de plusieurs corpus.
* Analyse temporelle des mots et Word Clouds.
* Interface Jupyter Notebook conviviale et modulaire.

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
- *Corpus.py*, *Document.py*, *DocumentFactory.py*, *Author.py* et *SearchEngine.py* → classes utilisées pour le corpus.
- *interface.py* → Construction de l'interface utilisateur.
- *UserInterface.ipynb* → Interface finale, fichier que doit exécuter l'utilisateur.
- *api_corpus.py* → Requêtes API, création du corpus et enregistrement de celui en .csv.
- *data.csv* → Exemple de produit de *api_corpus.py*, exploitable par *interface.py*.

## Prérequis

* **Python 3.9 ou plus**
* `pip` installé
* Connexion Internet (API Reddit, ArXiv, ressources NLTK)

installer les ibliothèques utilisées :
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

## Installation
### 1 - Cloner ou récupérer le projet

```bash
git clone https://github.com/Nirsenn/python-project
cd python-project
```
Ou dézipper l’archive du projet et se placer dans le dossier.

### 2 -  Installer les dépendances

```bash
pip install -r requirements.txt
```

## Ressources NLTK
Lors de la **première exécution**, le projet télécharge automatiquement :
* `punkt_tab`
* `stopwords`
NB: Une connexion Internet est nécessaire la première fois.

## Lancer le projet
Via **un environnement de développement intégré (IDE), par exemple VS Code** :

Puis ouvrir le notebook principal du projet:

`UserInterface.ipynb` et  executer le premier bloc de code pour lancer l'interface via le notebook.


## Interface interactive

Aperçu de l’interface Jupyter Notebook permettant l’exploration et la recherche dans le corpus :

![Interface Jupyter Notebook](images/Interface.png)


## Lien vers le rapport

 [Accéder au rapport du projet](https://docs.google.com/document/d/1hgUCek0he4WxjKjYceFKAqiJ4tZ-Qe0lW4a-XYOyQnE/edit?usp=sharing)


## Licence

Projet à usage pédagogique.


© Ce projet constitue une synthèse progressive des notions abordées tout au long des TDs de Programmation de Spécialité en Python.

