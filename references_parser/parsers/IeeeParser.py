from .SsauParser import SsauParser

SEP = ', '


class IEEEParser(SsauParser):
    """
    Parses Bibtext into IEEE citation format.
    Official citation guideline:
    https://ieee-dataport.org/sites/default/files/analysis/27/IEEE%20Citation%20Guidelines.pdf
    """
    def parse_article(self, bibtex_entry: dict):
        """
        Parse bibtex annotated with @article
        """
        authors = self._parse_authors(bibtex_entry['author'])
        title = bibtex_entry['title']
        year = bibtex_entry['year']

        journal = bibtex_entry['journal']

        result = authors + SEP + "\"" + title + ",\" " + journal

        if 'arXiv' in journal:
            result += SEP + f"{year}."
            return result

        number = "" if 'number' not in bibtex_entry else f"no. {bibtex_entry['number']}"
        volume = "" if 'volume' not in bibtex_entry else f"vol. {bibtex_entry['volume']}"
        if len(volume) != 0:
            result += SEP + volume
            result += SEP + number

        pages = bibtex_entry['pages'].split("--")
        if len(pages) == 1:
            result += SEP + f"p. {pages[0]}"
        elif len(pages) == 2:
            result += SEP + f"pp. {pages[0]}-{pages[1]}"

        result += SEP + f"{year}."
        return result

    def parse_proceedings(self, bibtex_entry: dict):
        """
        Parse bibtex annotated with @inproceedings
        """
        authors = self._parse_authors(bibtex_entry['author'])
        title = bibtex_entry['title']
        booktitle = bibtex_entry['booktitle']
        year = bibtex_entry['year']
        pages = [] if 'pages' not in bibtex_entry else bibtex_entry['pages'].split("--")

        result = authors + SEP + "\"" + title + ",\" In " + booktitle + SEP + year
        if len(pages) == 1:
            result += SEP + f"p. {pages[0]}"
        elif len(pages) == 2:
            result += SEP + f"pp. {pages[0]}-{pages[1]}"

        return result + "."

    def _parse_authors(self, authors):
        first_author, authors = super()._parse_authors(authors, return_all=True)

        authors_list = authors.split(', ')
        if len(authors_list) == 1:
            return authors
        if len(authors_list) == 2:
            return authors_list[0] + ' and ' + authors_list[1]
        # Add `and` before the last author
        authors_upd = ''
        for author in authors_list[:-1]:
            authors_upd += author + ', '
        authors_upd += 'and ' + authors_list[-1]
        return authors_upd
