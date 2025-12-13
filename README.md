# Projet Programmation de Spécialité – Python 

**Auteur :** Aissatou Lamarana Barry et Nissrine Ben Ayou
**Année :** 2025-2026  
**Enseignant :** Tetiana Yemelianenko 

Ce projet rassemble les travaux réalisés dans le cadre des TDs de **Programmation de Spécialité (Python)**.  
L’objectif global est de **collecter, analyser et explorer des corpus de documents** de manière interactive et conviviale.

---

## Objectifs

- Collecter des documents depuis différentes sources : CSV, API, web scraping.  
- Structurer les documents et les auteurs pour faciliter l’analyse.  
- Nettoyer et prétraiter les textes (ponctuation, chiffres, casse).  
- Construire un corpus et effectuer des analyses textuelles (statistiques, concordancier).  
- Implémenter un moteur de recherche par mots-clés avec scores TF et TF-IDF.  
- Créer une interface interactive dans Jupyter Notebook pour la recherche, la visualisation et la comparaison des corpus.  
- Observer l’évolution temporelle des mots et générer des Word Clouds.

---

## TDs et fonctionnalités

### TD3 – Extraction et prétraitement des données
- **Collecte de données** via fichiers CSV, API externes et web scraping (ex. Reddit, Arxiv).  
- Découpage des textes en phrases ou mots.  
- Construction d’un vocabulaire du corpus et premières statistiques.  

### TD4 – Structuration des documents
- Classes `Document` et `Author` pour gérer les textes et les auteurs.  
- Classe `Corpus` pour regrouper les documents, trier et explorer les données.
- Autres Classes, voir projet.

### TD5 – Héritage et polymorphisme
- Gestion de types spécifiques de documents (`RedditDocument`, `ArxivDocument`).  
- Exploitation du polymorphisme pour manipuler différents documents de manière uniforme.

### TD6 – Analyse textuelle
- Recherche de mots-clés et expressions via **expressions régulières**.  
- Construction d’un **concordancier** pour visualiser le contexte des mots.  
- Statistiques textuelles : comptage des mots, fréquence par document et dans le corpus.  

### TD7 – Moteur de recherche
- Construction d’une **matrice Documents × Termes**.  
- Calcul des scores **TF** et **TF-IDF**.  
- Recherche par mots-clés avec vecteurs de requête et mesure de similarité (produit scalaire ou cosinus).  
- Résultats présentés sous forme de **DataFrame**.

### TD8 – Interface Jupyter Notebook
- Découpage des textes longs en phrases.  
- Recherche interactive avec filtres : auteur, type de document, année.  
- Affichage dynamique des résultats avec `widgets` (`Text`, `IntSlider`, `Button`, `Output`).  

### TD9 et TD10 – Interface avancée et exploration comparative
- Comparaison de deux corpus (Reddit vs Arxiv) : mots spécifiques ou communs.  
- Visualisation de l’évolution temporelle des mots.  
- Génération de **Word Clouds** interactifs.  
- Possibilité de filtrer les recherches par auteur, type de document ou période.

---

## Fonctionnalités principales

- Collecte et extraction de données : CSV, API, web scraping.  
- Gestion et exploration de documents et auteurs.  
- Nettoyage et prétraitement des textes.  
- Analyse textuelle avancée (TF, TF-IDF, concordancier).  
- Moteur de recherche interactif avec filtres.  
- Comparaison et visualisation de corpus multiples.  
- Visualisation temporelle des mots et génération de Word Clouds.  
- Interface Jupyter Notebook conviviale et modulaire.

---

Lien vers le rapport : https://docs.google.com/document/d/1hgUCek0he4WxjKjYceFKAqiJ4tZ-Qe0lW4a-XYOyQnE/edit?usp=sharing
