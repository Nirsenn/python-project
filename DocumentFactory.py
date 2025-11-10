import Document

class DocumentFactory:
    @staticmethod
    def createDocument(source, titre, auteur, date, url, texte, extra):
        # source : "reddit" ou "arxiv"
        #extra : nb_comment (int) pour Reddit, coAuteur (list) pour Arxiv
        source = source.lower()

        if source == "reddit":
            return Document.RedditDocument(titre, auteur, date, url, texte, nb_comment=extra, type="Reddit")
        elif source == "arxiv":
            return Document.ArxivDocument(titre, auteur, date, url, texte, coAuteur=extra, type="Arxiv")
        else:
            raise ValueError("Source inconnue. Choisir 'reddit' ou 'arxiv'.")
