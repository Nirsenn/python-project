# Ce fichier permert de créer un corpus et de l'enregistrer au format csv. Sa construction est faite à partir de contenu provenant de Reddit et Arxiv avec des requêtes API

#Requirements :
import praw
from datetime import datetime
import requests
import xmltodict
import dateutil.parser as dp
import Author
import Document
import Corpus
import importlib
importlib.reload(Document)
importlib.reload(Author)
importlib.reload(Corpus)

# Boucle pour récupérer des documents Reddit

#instanciation de l'authentification aux outils API de Reddit
reddit = praw.Reddit(client_id='WhOeUX8xCa_LSqqzHogeNA', client_secret='IouRe-5putFpKpyr11rOW7Wzh2Rpmw', user_agent='Web Scrapping')

#Les 10 posts les plus tendance du subreddit MachineLearning :
hot_posts = [
    p for p in reddit.subreddit('MachineLearning').hot(limit=20)
    if p.author and p.author.name != "AutoModerator"
    and p.selftext and len(p.selftext) > 700 and "arxiv.org" not in p.url
]

#variables principales
docs = []                 #stocke les données d'un article (indice 0 → titre, 1 → auteur, 2 → date de publication, 3 → url, 4 → contenu textuel)
origines = []             #tableau indiquant l'origine du document (Reddit ou Arxiv)
id2doc = {}               #Clés : id du document, Valeurs : objet Document
id2aut = {}               #Clés : noms des auteurs, Valeurs : id des documents publiés
id = 1                    #id du document

#pour chaque post Reddit
for posts in hot_posts:
  docs.append(posts.title)                #ajout du titre dans docs
  auteurs = posts.author.name             #ajout du nom d'auteur dans docs
  docs.append(auteurs)

  texte = posts.selftext                  #contenu texte
  texte = texte.replace("\n", " ")                #formatage du texte pour remplacer les sauts de ligne \n par un espace
  texte = texte.replace("\t", " ")
  texte = texte.replace(";", " ")
  texte = texte.replace("&#x200B", "")
  if texte == "":                         #Pour les contenu textuels vides, ils seront rreprésentés par un espace afin de pouvoir être traités par les fonctions du corpus
    texte = " "


  if auteurs not in id2aut.keys():        #vérification de la présence de l'auteur dans id2aut
    id2aut[auteurs] = Author.Author(auteurs)  #instanciation de l'objet Author avec le nouvel auteur
    id2aut[auteurs].add(id, texte)
  else:
    id2aut[auteurs].add(id, texte)           #ajout du document à la production de l'auteur

  dateP = posts.created_utc               #ajout de la date dans docs au format unix
  docs.append(datetime.fromtimestamp(dateP))

  docs.append(posts.url)                  #ajout de l'url dans docs

  docs.append(texte)                      #ajout du contenu texte dans docs
  docs.append(posts.num_comments)         #ajout du nombre commentaire dans docs

  docs.append("Reddit")                   #récupération de l'origine du post

  print(f"Ajout Reddit id={id} titre={posts.title}")

  #Une fois toutes les données du post récupérées, on instancie l'objet Document dans id2doc avec un id unique
  id2doc[id] = Document.RedditDocument(docs[0], docs[1], docs[2], docs[3], docs[4], docs[5], docs[6])
  id+=1                                   #incrémentation de l'id
  docs = []                               #on vide le tableau pour pouvoir ajouter les données du document suivant

# Boucle pour récupérer des documents Arxiv

#url contenant la requete (ici, 10 articles résultant de la recherche des mots Machine et Learning).
url = 'http://export.arxiv.org/api/query?search_query=all:machine+learning&start=0&max_results=10'

data = requests.get(url)                      #Obtention des données au format XML à partir de la requête
articles = xmltodict.parse(data.text)         #données converties du format XML à dictionnaire

#parcours des articles
entries = articles['feed']['entry']
for entry in entries:
  a2 = [] #tableau des coauteurs
  docs.append(entry.get("title"))             #ajout du titre dans docs

  summary = entry['summary']                  #contenu textuel
  summary = summary.replace("\n", " ")
  summary = summary.replace("\t", " ")                  #formatage du texte pour remplacer les sauts de ligne \n par un espace
  summary = summary.replace(";", " ")
  summary = summary.replace("&#x200B", "")

  authors = entry.get("author", [])           #ajout de l'auteur dans docs
  if type(authors) is dict:                   #si un seul auteur
    a = authors.get("name") #a = premier auteur
    if a not in id2aut.keys():                #vérification de la présence de l'auteur dans id2aut
      id2aut[a] = Author.Author(a)  #instanciation de l'objet AUthor avec le nouvel auteur
      id2aut[a].add(id, summary)
    else:
      id2aut[a].add(id, summary)
    docs.append(a)
  else:                                       #si plusieurs auteurs
    docs.append(authors[0].get("name"))
    for au in authors:
      a2.append(au.get("name"))
      if au.get("name") not in id2aut.keys(): #vérification de la présence de l'auteur dans id2aut
        id2aut[au.get("name")] = Author.Author(a2)
        id2aut[au.get("name")].add(id, summary)
      else:
        id2aut[au.get("name")].add(id, summary)
    a2 = a2[1:]                              #on met la lste des co-auteurs dans a2 (donc tous sauf le premier element)

  dateP = entry.get("published")              #ajout de la date de publication dans docs au format unix
  dateP = dp.parse(dateP)
  dateP = dateP.timestamp()
  docs.append(datetime.fromtimestamp(dateP))

  url = entry.get("id")                       #ajout de l'url dans docs
  docs.append(url)

  docs.append(summary)                        #ajout du contenu textuel dans docs

  docs.append(a2)

  docs.append("Arxiv")                        #récupération de l'origine du post

  print(f"Ajout Arxiv id={id} titre={entry.get('title')}")

  #Une fois toutes les données du post récupérées, on instancie l'objet Document dans id2doc avec un id unique
  id2doc[id] = Document.ArxivDocument(docs[0], docs[1], docs[2], docs[3], docs[4], docs[5], docs[6])
  docs = []                                   ##on vide le tableau pour pouvoir ajouter les données du document suivant
  id+=1                                       #incrémentation de l'id

# Création du corpus
corpus = Corpus.Corpus("Machine Learning", id2aut, id2doc)

# Enregistrement du corpus au format csv
corpus.save("data.csv")
print(corpus)
