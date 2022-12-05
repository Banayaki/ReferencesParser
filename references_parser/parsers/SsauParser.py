import bibtexparser as p

# Constant which stands for the following template: ". (long dash) " or ". -- "
SEP_DASH = u". \u2012 "


class SsauParser:

    def parse_article(self, bibtex_entry: dict):
        """
        Parse bibtex annotated with @article
        """
        first_author, authors = self._parse_authors(bibtex_entry['author'])
        title = bibtex_entry['title']
        year = bibtex_entry['year']

        try:
            journal = bibtex_entry['journal']
            if 'arXiv' in journal:
                raise Exception("Reference from ARXIV")
        except:
            # In case of reference on arxiv.org
            # TODO: replace with correct Arxiv reference, for example:
            # Kingma, D.P. Adam: A method for stochastic optimization [Электронный ресурс] / D.P. Kingma, J. Ba // ArXiv. – 2014. – URL: https://arxiv.org/abs/1412.6980 (дата обращения: 01.05.2021).
            return first_author + " " + title + " [Текст] / " + authors + " // ArXiv" + SEP_DASH + year + "."

        result = first_author + " " + title + " [Текст] / " + authors + " // " + journal + SEP_DASH + year

        number = "" if 'number' not in bibtex_entry else f"({bibtex_entry['number']})"
        volume = "" if 'volume' not in bibtex_entry else f"Vol. {bibtex_entry['volume']}{number}"
        if len(volume) != 0:
            result += SEP_DASH + volume

        pages = [] if 'pages' not in bibtex_entry else bibtex_entry['pages'].split("--")
        if len(pages) == 0:
            pass
        elif len(pages) == 1:
            result += SEP_DASH + f"P. {pages[0]}"
        elif len(pages) == 2:
            result += SEP_DASH + f"P. {pages[0]}-{pages[1]}"
        return result + "."

    def parse_proceedings(self, bibtex_entry: dict):
        """
        Parse bibtex annotated with @inproceedings
        """
        first_author, authors = self._parse_authors(bibtex_entry['author'])
        title = bibtex_entry['title']
        booktitle = bibtex_entry['booktitle']
        year = bibtex_entry['year']
        pages = [] if 'pages' not in bibtex_entry else bibtex_entry['pages'].split("--")
        org_year = year if 'organization' not in bibtex_entry else f"{bibtex_entry['organization']}, {year}"

        result = first_author + " " + title + " [Текст] / " + authors + " // " + booktitle + SEP_DASH + org_year
        if len(pages) == 1:
            result += SEP_DASH + f"P. {pages[0]}"
        elif len(pages) == 2:
            result += SEP_DASH + f"P. {pages[0]}-{pages[1]}"

        return result + "."

    def _parse_authors(self, author_string, return_all=False):
        def parse_single_author(str_author):
            result = ""
            splitted_author = p.customization.splitname(str_author)
            for initial in splitted_author['first']:
                result += initial[0] + "."
            return result + " " + "".join(splitted_author['last']) + ", "

        authors = ""
        first_author = ""

        first_author_unparsed = author_string[0]
        splitted_first_author = p.customization.splitname(first_author_unparsed)
        first_author += "".join(splitted_first_author['last']) + ", "
        for initial in splitted_first_author['first']:
            first_author += initial[0]
        first_author += "."

        if len(author_string) < 5 or return_all:
            for str_author in author_string:
                authors += parse_single_author(str_author)
            authors = authors[:-2]
        else:
            authors = f"{parse_single_author(author_string[0])[:-2]} [и др.]"
        return first_author, authors

    def __call__(self, bibtex: str):
        if bibtex.endswith('.txt'):
            with open(bibtex, 'r') as f:
                bibtex_dict = p.load(f)
        else:
            bibtex_dict = p.loads(bibtex)
        result = []
        for bibtex_entry in bibtex_dict.entries:
            # The following line will parse string with authors in list of authors
            bibtex_entry = p.customization.author(bibtex_entry)
            bibtex_entry = p.customization.convert_to_unicode(bibtex_entry)
            if bibtex_entry['ENTRYTYPE'] == "article":
                result.append(self.parse_article(bibtex_entry))
            elif bibtex_entry['ENTRYTYPE'] == "inproceedings":
                result.append(self.parse_proceedings(bibtex_entry))
            else:
                raise Exception(f"Unsupported bibtex type: {bibtex_entry['ENTRYTYPE']}")
        return result
