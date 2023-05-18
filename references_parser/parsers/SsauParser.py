from datetime import datetime
from duckpy import Client

import bibtexparser as p

# Constant which stands for the following template: ". (long dash) " or ". -- "
SEP_DASH = ". \u2012 "


class SsauParser:
    
    def __init__(self):
        self.search_client = Client()
    
    def parse_website(self, bibtex_entry: dict):
        result = bibtex_entry["title"]
        
        base = bibtex_entry.get("base")
        year = bibtex_entry["year"]
        origin = bibtex_entry["origin"]
        url = bibtex_entry["url"]
        date = bibtex_entry["date"]
        address = bibtex_entry.get("address")
        
        if base and len(base) > 0:
            result += " // " + base
        result += " / " + origin
        if address is None:
            result += SEP_DASH + "[Б.м.], " + year
        else:
            result += SEP_DASH + f"{address}, " + year
        result += SEP_DASH + "URL: "
        result += url
        result += f" (дата обращения: {date})"
        return result
    
    def parse_arxiv(self, bibtex_entry: dict):
        """
        In case of reference on arxiv.org
        Le, Q. Distributed Representations of Sentences and Documents / Q. Le,
        T. Mikolov // ArXiv / Cornell University. – 2014. – URL: https://arxiv.org/abs/1405.4053 (дата обращения: 03.11.2020)
        """
        first_author, authors = self._parse_authors(bibtex_entry["author"])
        title = bibtex_entry["title"]
        year = bibtex_entry["year"]
        
        url = bibtex_entry.get("url")
        today = datetime.now().strftime('%d.%m.%Y')
        
        if url is None:
            results = self.search_client.search(f"arxiv {title}")
            url = results[0]['url']
            
        result = ""
        if first_author is not None:
            result += first_author + " "
        
        return (
            result
            + title
            + " / "
            + authors
            + " // ArXiv / Cornell University"
            + SEP_DASH
            + year
            + SEP_DASH
            + f"URL: {url} (дата обращения: {today})"
            )

    def parse_article(self, bibtex_entry: dict):
        """
        Parse bibtex annotated with @article
        """
        try:
            journal = bibtex_entry["journal"]
            if "arXiv" in journal:
                raise Exception("Reference from ARXIV")
        except:
            return self.parse_arxiv(bibtex_entry)
        
        first_author, authors = self._parse_authors(bibtex_entry["author"])
        title = bibtex_entry["title"]
        year = bibtex_entry["year"]
        
        result = ""
        if first_author is not None:
            result += first_author + " "

        result = (
            result
            + title
            + " / "
            + authors
            + " // "
            + journal
            + SEP_DASH
            + year
        )

        number = "" if "number" not in bibtex_entry else f"({bibtex_entry['number']})"
        volume = (
            ""
            if "volume" not in bibtex_entry
            else f"Vol. {bibtex_entry['volume']}{number}"
        )
        if len(volume) != 0:
            result += SEP_DASH + volume

        pages = [] if "pages" not in bibtex_entry else bibtex_entry["pages"].split("--")
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
        first_author, authors = self._parse_authors(bibtex_entry["author"])
        title = bibtex_entry["title"]
        booktitle = bibtex_entry["booktitle"]
        year = bibtex_entry["year"]
        pages = [] if "pages" not in bibtex_entry else bibtex_entry["pages"].split("--")
        org_year = (
            year
            if "organization" not in bibtex_entry
            else f"{bibtex_entry['organization']}, {year}"
        )
        
        result = ""
        if first_author is not None:
            result += first_author + " "

        result = (
            result
            + title
            + " / "
            + authors
            + " // "
            + booktitle
            + SEP_DASH
            + org_year
        )
        if len(pages) == 1:
            result += SEP_DASH + f"P. {pages[0]}"
        elif len(pages) == 2:
            result += SEP_DASH + f"P. {pages[0]}-{pages[1]}"

        return result + "."

    def _parse_authors(self, author_string, return_all=False):
        """
        1. Авторов < 4
        Фамилия, инициалы первого автора. Основное заглавие : 
        добавочное заглавие / Инициалы и фамилии первого, 
        второго, третьего автора
        2. Авторов == 4
        Основное заглавие : добавочное заглавие / Инициалы и 
        фамилии всех четырех авторов ;
        3. Авторов > 4
        Основное заглавие : добавочное заглавие / Инициалы и 
        фамилии первых трех авторов [и др.]
        """
        def parse_single_author(str_author):
            result = ""
            splitted_author = p.customization.splitname(str_author)
            for initial in splitted_author["first"]:
                result += initial[0] + "."
            return result + " " + "".join(splitted_author["last"]) + ", "

        authors = ""
        first_author = ""

        first_author_unparsed = author_string[0]
        splitted_first_author = p.customization.splitname(first_author_unparsed)
        first_author += "".join(splitted_first_author["last"]) + ", "
        for initial in splitted_first_author["first"]:
            first_author += initial[0]
        first_author += "."

        if len(author_string) < 4 or return_all:
            for str_author in author_string:
                authors += parse_single_author(str_author)
            authors = authors[:-2]
        elif len(author_string) == 4:
            for str_author in author_string:
                authors += parse_single_author(str_author)
            authors = authors[:-2]
            first_author = None
        else:
            for str_author in author_string[:3]:
                authors += parse_single_author(str_author)
            authors = authors[:-2]
            first_author = None
            authors = f"{authors} [и др.]"
        return first_author, authors

    def __call__(self, bibtex: str):
        if bibtex.endswith(".txt"):
            with open(bibtex, "r") as f:
                bibtex_dict = p.load(f, p.bparser.BibTexParser(ignore_nonstandard_types=False))
        else:
            bibtex_dict = p.loads(bibtex, p.bparser.BibTexParser(ignore_nonstandard_types=False))
        result = []
        for bibtex_entry in bibtex_dict.entries:
            # The following line will parse string with authors in list of authors
            bibtex_entry = p.customization.author(bibtex_entry)
            bibtex_entry = p.customization.convert_to_unicode(bibtex_entry)
            bibtex_type = bibtex_entry["ENTRYTYPE"]
            if bibtex_type == "article":
                result.append(self.parse_article(bibtex_entry))
            elif bibtex_type == "inproceedings":
                result.append(self.parse_proceedings(bibtex_entry))
            elif bibtex_type == "online":
                result.append(self.parse_website(bibtex_entry))
            else:
                raise Exception(f"Unsupported bibtex type: {bibtex_entry['ENTRYTYPE']}")
        return result
