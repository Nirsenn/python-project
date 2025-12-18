# Ce fichier permet le chargement d'un fichier data.csv sous forme de corpus contenant des documents Reddit et Arxiv et de construction l'interface pour l'utilisateur

import Corpus
import Document
import DocumentFactory
import SearchEngine
from dateutil import parser
import importlib
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
importlib.reload(Corpus)
importlib.reload(Document)
importlib.reload(DocumentFactory)
importlib.reload(SearchEngine)

# Chargement du fichier data(Arxiv - Reddit)
df = pd.read_csv("data.csv", sep="\t")
pd.set_option('display.max_colwidth', None)

# re-initialiser les params
id2doc = {} # documents de tout le corpus
id2docReddit = {} # documents reddit
id2docArxiv = {} # documents arxiv
autR = {} # auteurs reddit
autA = {} # auteurs arxiv

for index, row in df.iterrows():
    dtype = row['type']
    titre = row['titre']
    auteur = row['auteur']
    date = parser.parse(row['date'])
    texte = row['texte']
    url = row['url']
    if row['type'] == "Reddit":
      nb_comment = row['nb_comment']
    elif row['type'] == "Arxiv":
      coAuteur = row['coAuteur'].split(",") if 'coAuteur' in row else None


    # Céer le Document Object
    doc = DocumentFactory.DocumentFactory.createDocument(dtype, titre, auteur, date, url, texte, "")
    if dtype == "Reddit":
      id2docReddit[row['id']] = doc
      autR[auteur] = 1 if auteur not in autR.keys() else autR[auteur] + 1
    elif dtype == "Arxiv":
      id2docArxiv[row['id']] = doc
      autA[auteur] = 1 if auteur not in autA.keys() else autA[auteur] + 1
    id2doc[row['id']] = doc

aut = df.auteur.value_counts().to_dict()

# Instanciation des objets corpus, corpusArxiv, corpusReddit

corpus = Corpus.Corpus("Machine Learning", aut, id2doc)
corpus.ndoc = len(corpus.id2doc)
corpus.naut = len(corpus.authors)

corpusArxiv = Corpus.Corpus("Arxiv", autA, id2docArxiv)
corpusArxiv.ndoc = len(corpusArxiv.id2doc)
corpusArxiv.naut = len(corpusArxiv.authors)

corpusReddit = Corpus.Corpus("Reddit", autR, id2docReddit)
corpusReddit.ndoc = len(corpusReddit.id2doc)
corpusReddit.naut = len(corpusReddit.authors)

texte_joinA=""
texte_joinR=""
texte_join =""

for texte in corpusReddit.id2doc.values():
  texte_joinR += texte.texte #rassemble le texte de chaque document
for texte in corpusArxiv.id2doc.values():
  texte_joinA += texte.texte #rassemble le texte de chaque document Arxiv
for texte in corpus.id2doc.values():
  texte_join += texte.texte #rassemble le texte de chaque document Reddit

# Fonction de nettoyage du texte join et suppression des stopwords

def clean_doc(texte):
  texte = texte.lower()
  #tokenisation du texte
  tokens = word_tokenize(texte)

  # retire tous les token qui ne sont pas des mots (ponctuation etc)
  txt = [word for word in tokens if word.isalpha()]

  # initialize une liste des stop words anglais pour les retirer des tokens
  stop_words = set(stopwords.words('english'))
  mots = [w for w in txt if not w in stop_words]

  # on retire les token à un seul caractère
  mots = [w for w in mots if len(w)>1]

  # Renvoie une chaine et pas une liste
  return " ".join(mots)

# Textes tokenizés et nettoyés
cleanArxiv = clean_doc(texte_joinA)
cleanReddit = clean_doc(texte_joinR)
cleanAll = clean_doc(texte_join)


# Préparer le dataFrame de comparaison
freqA = Counter(cleanArxiv.split()) # Decoupe la chaine join, compte l'occurence de chaque mot et retourne un dictionnaire mot:occurence
freqR = Counter(cleanReddit.split())

mots_union = set(freqA.keys()) & set(freqR.keys())  # Verifier une intersection entre les deux ensembles (Arxiv - Reddit)
data = []
for mot in mots_union:
    data.append({
        "mot": mot,
        "freq_arxiv": freqA.get(mot, 0), # la fonction get recupere la valeur(freq) de la clé mot
        "freq_reddit": freqR.get(mot, 0),
    })
df_compare = pd.DataFrame(data)

# Fontions d'evolution temporelle en fonction de l'année
def evolution_temporelle(mot, corpus):
    freq_par_annee = {}
    for doc in corpus.id2doc.values():
        an = int(str(doc.date)[:4])
        txt = corpus.nettoyer_texte(doc.texte).split()
        if mot in txt:
            freq_par_annee[an] = freq_par_annee.get(an, 0) + txt.count(mot)
    return freq_par_annee

search = SearchEngine.SearchEngine(corpus)

from IPython.display import display, clear_output
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout
from wordcloud import WordCloud

# 1- Widgets interface

# Recherche documents
text_requete = widgets.Text(description="Mots clés :")
slider_n = widgets.IntSlider(value=5, min=1, max=20, step=1, description="Nb doc:")
auteur_widget = widgets.Dropdown(options=["Tous"] + list(corpus.authors.keys()), value="Tous", description="Auteur :")
type_widget = widgets.Dropdown(options=["Tous", "Reddit", "Arxiv"], value="Tous", description="Type :")
date_widget = widgets.Text(value="", description="Année :", placeholder="Ex: 2023")
bouton_recherche = widgets.Button(description="Rechercher", button_style="info")
output = widgets.Output()

# Comparaison Arxiv vs Reddit
select_type_compare = widgets.Dropdown(
    options=["Mots spécifiques Arxiv", "Mots spécifiques Reddit", "Mots communs"],
    value="Mots spécifiques Arxiv",
    description="Comparer :"
)
slider_top = widgets.IntSlider(value=20, min=5, max=100, step=5, description="Top N mots :")
bouton_compare = widgets.Button(description="Afficher comparaison", button_style="info")
output_compare = widgets.Output()

# Évolution temporelle
text_mot = widgets.Text(description="Mot :")
select_corpus = widgets.Dropdown(options=["Arxiv", "Reddit", "Tous"], description="Corpus :")
bouton_evo = widgets.Button(description="Tracer évolution", button_style="warning")
output_evo = widgets.Output()

# Nuage cloud
select_corpus_wc = widgets.Dropdown(options=["Arxiv", "Reddit", "Tous"], description="Corpus WC :")
slider_top_wc = widgets.IntSlider(value=100, min=10, max=300, step=10, description="Top N mots :")
bouton_wc = widgets.Button(description="Afficher Word Cloud", button_style="success")
output_wc = widgets.Output()

# Recherche de mots dans un passage
text_concorde = widgets.Text(description="Mot :")
slider_concorde = widgets.IntSlider(value=30, min=10, max=100, step=5, description="Taille contexte :")
select_corpus_concorde = widgets.Dropdown(options=["Arxiv", "Reddit", "Tous"], description="Corpus :")
bouton_concorde = widgets.Button(description="Afficher concordance", button_style="primary")
output_concorde = widgets.Output()

# Réinitialiser l'interface
bouton_close = widgets.Button(description="Fermer l'application", button_style='danger')


# 2- Fonctions boutons

#Recherche
def clique_bouton_recherche(b):
    with output:
        clear_output()
        requete = text_requete.value
        n_docs = slider_n.value
        auteur = auteur_widget.value
        types = type_widget.value
        annee = date_widget.value.strip() if isinstance(date_widget.value, str) else ""

        # IDs filtrés
        ids_filtres = [
            doc_id for doc_id, doc in corpus.id2doc.items()
            if (auteur=="Tous" or doc.auteur==auteur)
            and (annee=="" or str(doc.date)[:4]==annee)
            and (types=="Tous" or doc.type==types)
        ]

        # Appel direct du moteur de recherche
        resultat = search.moteurRechercheFiltre(requete, ids_filtres, n=n_docs)
        if resultat.empty:
            print("Aucun résultat trouvé.")
        else:
            display(resultat)  # Affiche directement le DataFrame

#Comparaison
def afficher_comparaison(b):
    with output_compare:
        clear_output()
        df = df_compare.copy()
        choix = select_type_compare.value
        topN = slider_top.value
        if choix=="Mots spécifiques Arxiv": # mots specifiques Arxiv
            df = df[df["freq_arxiv"] > 2*df["freq_reddit"]].sort_values("freq_arxiv", ascending=False)
        elif choix=="Mots spécifiques Reddit": # mots specifiques Reddit
            df = df[df["freq_reddit"] > 2*df["freq_arxiv"]].sort_values("freq_reddit", ascending=False)
        else:  # mots communs
            df = df[(df["freq_arxiv"]>0) & (df["freq_reddit"]>0)].sort_values("mot")
        display(df.head(topN))

#Evolution d'un mot
def tracer_evolution_widget(b):
    with output_evo:
        clear_output()
        mot = text_mot.value.strip()
        mot = mot.lower()
        corpus_sel = corpusArxiv if select_corpus.value=="Arxiv" else corpusReddit if select_corpus.value=="Reddit" else corpus
        if mot:
            freq = evolution_temporelle(mot, corpus_sel)
            if not freq:
                print(f"Aucune occurrence trouvée pour '{mot}'")
            else:
                plt.figure(figsize=(8,4))
                plt.bar(freq.keys(), freq.values(), color='skyblue')
                plt.title(f"Évolution temporelle du mot '{mot}'")
                plt.xlabel("Année")
                plt.ylabel("Fréquence")
                plt.show()
        else:
            print("Veuillez entrer un mot :")

#Nuage de mots
def afficher_wordcloud(corpus_sel, top_n=100):
    if corpus_sel == corpusArxiv:
        texte_total = cleanArxiv
    elif corpus_sel == corpusReddit:
        texte_total = cleanReddit
    else:
        texte_total = cleanAll

    # Générer le Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white", max_words=top_n).generate(texte_total)

    # Affichage
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def afficher_wordcloud_widget(b):
    with output_wc:
        clear_output()
        corpus_sel = corpusArxiv if select_corpus_wc.value=="Arxiv" else corpusReddit if select_corpus_wc.value=="Reddit" else corpus
        afficher_wordcloud(corpus_sel, top_n=slider_top_wc.value)

def afficher_concorde(b):
    with output_concorde:
        clear_output()
        mot = text_concorde.value.strip()
        taille = slider_concorde.value
        corpus_sel = corpusArxiv if select_corpus_concorde.value=="Arxiv" else corpusReddit if select_corpus_concorde.value=="Reddit" else corpus

        if mot:
            corpus_sel.concorde(" ".join([doc.texte for doc in corpus_sel.id2doc.values()]), mot, taille)
        else:
            print("Veuillez entrer un mot :")


def fermer_app(b):
    text_requete.value = ""
    slider_n.value = 5
    auteur_widget.value = "Tous"
    type_widget.value = "Tous"
    date_widget.value = ""
    text_mot.value = ""
    select_corpus.value = "Arxiv"
    output.clear_output()
    output_compare.clear_output()
    output_evo.clear_output()
    output_wc.clear_output()
    output_concorde.clear_output()


# 3- Lier les boutons avec les fonctions
bouton_recherche.on_click(clique_bouton_recherche)
bouton_compare.on_click(afficher_comparaison)
bouton_evo.on_click(tracer_evolution_widget)
bouton_wc.on_click(afficher_wordcloud_widget)
bouton_concorde.on_click(afficher_concorde)
bouton_close.on_click(fermer_app)


# 4- Affichage interface
col_layout = Layout(
    width='50%',
    min_width='250px',
    border='1px solid lightgray',
    padding='5px')

# Colonne Comparaison
col_comparaison = VBox([
    widgets.Label(" Comparaison Arxiv vs Reddit"),
    select_type_compare,
    slider_top,
    bouton_compare,
    output_compare
], layout=col_layout)

# Colonne Évolution
col_evolution = VBox([
    widgets.Label(" Évolution temporelle d'un mot"),
    text_mot,
    select_corpus,
    bouton_evo,
    output_evo
], layout= col_layout)

# Colonne Nuage de mots
col_wordcloud = VBox([
    widgets.Label(" Word Cloud"),
    select_corpus_wc,
    slider_top_wc,
    bouton_wc,
    output_wc
], layout=col_layout)

# Colonne Recherche
col_recherche = VBox([
    widgets.Label(" Recherche de documents"),
    text_requete,
    slider_n,
    auteur_widget,
    type_widget,
    date_widget,
    bouton_recherche,
    output
], layout= col_layout)

col_concorde = VBox([
    widgets.Label(" Contexte"),
    text_concorde,
    slider_concorde,
    select_corpus_concorde,
    bouton_concorde,
    output_concorde
], layout=Layout(width='100%', border='1px solid lightgray', padding='5px'))


# Bouton fermer
section_close = VBox([bouton_close], layout=Layout(width='100%', align_items='center', margin='10px 0 0 0'))


# Titre et texte explicatif
titre = widgets.HTML(
    value="<h2>Interface d'analyse de corpus</h2>"
)

texte_intro = widgets.HTML(
    value="<p>Cette interface permet d'explorer un corpus de posts <a href='https://www.reddit.com/'>Reddit</a> et d'arcticles <a href='https://arxiv.org/'>Arxiv</a> à travers plusieurs fonctionnalités : </p>"
          "<ul><li>Recherche</li> <li>Comparaison entre les deux sources</li> <li>Evolution temporelle des mots</li> <li>Nuages de mots</li> <li>Contexte d'un mot dans un passage</li></ul>"
          "Utilisez les différents boutons pour interagir avec les données."
)

# Interface finale avec HBox pour afficher verticalement par deux colonnes
interface = VBox([
    titre,
    texte_intro,
    HBox([col_recherche,col_comparaison]),  # 2 colonnes alignées
    HBox([col_evolution,col_wordcloud]),  # 2 colonnes alignées
    HBox([col_concorde], layout=Layout(justify_content='center')),
    section_close
])

display(interface)
