from datetime import datetime
from typing import List, Optional

import bibtexparser as p
from duckpy import Client
from tqdm import tqdm

from references_parser.models import Bibtex, BibtexSsau

# Constant which stands for the following template: ". (long dash) " or ". -- "
SEP_DASH = ". \u2012 "


class SsauParser:
    def __init__(self):
        self.search_client = Client()
        self.errors = {}

    def parse_website(self, bibtex: BibtexSsau):
        result = bibtex.title

        if bibtex.base is not None and len(bibtex.base) > 0:
            result += " // " + bibtex.base
        result += " / " + bibtex.origin
        if bibtex.address is None:
            result += SEP_DASH + "[Б.м.], " + bibtex.year
        else:
            result += SEP_DASH + f"{bibtex.address}, " + bibtex.year
        result += SEP_DASH + "URL: "
        result += bibtex.url
        result += f" (дата обращения: {bibtex.date})."
        return result

    def parse_arxiv(self, bibtex: BibtexSsau):
        """
        In case of reference on arxiv.org
        Le, Q. Distributed Representations of Sentences and Documents / Q. Le,
        T. Mikolov // ArXiv / Cornell University. – 2014.
        – URL: https://arxiv.org/abs/1405.4053 (дата обращения: 03.11.2020)
        """
        first_author, authors = bibtex.get_parsed_authors()
        today = datetime.now().strftime("%d.%m.%Y")

        if bibtex.url is None:
            try:
                results = self.search_client.search(f"arxiv {bibtex.title}")
                url = results[0]["url"]
            except Exception as e:
                self.errors[bibtex.title] = {"Error occured while searching": str(e)}
                return None

        result = ""
        if first_author is not None:
            result += first_author + " "

        return (
            result
            + bibtex.title
            + " / "
            + authors
            + " // ArXiv / Cornell University"
            + SEP_DASH
            + bibtex.year
            + SEP_DASH
            + f"URL: {url} (дата обращения: {today})."
        )

    def parse_article(self, bibtex: BibtexSsau):
        """
        Parse bibtex annotated with @article
        """
        if bibtex.journal is not None and "arXiv" in bibtex.journal:
            return self.parse_arxiv(bibtex)

        first_author, authors = bibtex.get_parsed_authors()

        result = ""
        if first_author is not None:
            result += first_author + " "

        result = (
            result
            + bibtex.title
            + " / "
            + authors
            + " // "
            + bibtex.journal
            + SEP_DASH
            + bibtex.year
        )

        number = f"({bibtex.number})" if bibtex.number is not None else ""
        volume = f"Vol. {bibtex.volume}{number}" if bibtex.volume is not None else ""
        if len(volume) != 0:
            result += SEP_DASH + volume

        pages = bibtex.pages_list
        if len(pages) == 0:
            pass
        elif len(pages) == 1:
            result += SEP_DASH + f"P. {pages[0]}"
        elif len(pages) == 2:
            result += SEP_DASH + f"P. {pages[0]}-{pages[1]}"
        return result + "."

    def parse_proceedings(self, bibtex: BibtexSsau):
        """
        Parse bibtex annotated with @inproceedings
        """
        first_author, authors = bibtex.get_parsed_authors()
        org_year = (
            f"{bibtex.organization}, {bibtex.year}"
            if bibtex.organization is not None
            else bibtex.year
        )

        result = ""
        if first_author is not None:
            result += first_author + " "

        result = (
            result
            + bibtex.title
            + " / "
            + authors
            + " // "
            + bibtex.booktitle
            + SEP_DASH
            + org_year
        )

        number = f"({bibtex.number})" if bibtex.number is not None else ""
        volume = f"Vol. {bibtex.volume}{number}" if bibtex.volume is not None else ""
        if len(volume) != 0:
            result += SEP_DASH + volume

        pages = bibtex.pages_list
        if len(pages) == 0:
            pass
        elif len(pages) == 1:
            result += SEP_DASH + f"P. {pages[0]}"
        elif len(pages) == 2:
            result += SEP_DASH + f"P. {pages[0]}-{pages[1]}"
        return result + "."

    def __call__(self, bibtex: str) -> List[Optional[str]]:
        if bibtex.endswith(".txt"):
            with open(bibtex, "r") as f:
                bibtex_dict = p.load(
                    f, p.bparser.BibTexParser(ignore_nonstandard_types=False)
                )
        else:
            bibtex_dict = p.loads(
                bibtex, p.bparser.BibTexParser(ignore_nonstandard_types=False)
            )
        result = []
        for bibtex_entry in tqdm(bibtex_dict.entries):
            # The following line will parse string with authors in list of authors
            bibtex_entry = p.customization.author(bibtex_entry)
            bibtex_entry = p.customization.convert_to_unicode(bibtex_entry)

            bibtex_model = BibtexSsau(**bibtex_entry)

            if bibtex_model.ENTRYTYPE == Bibtex.Types.Article:
                result.append(self.parse_article(bibtex_model))
            elif bibtex_model.ENTRYTYPE == Bibtex.Types.Proceedings:
                result.append(self.parse_proceedings(bibtex_model))
            elif bibtex_model.ENTRYTYPE == Bibtex.Types.Website:
                result.append(self.parse_website(bibtex_model))
            else:
                raise Exception(f"Unsupported bibtex type: {bibtex_model.ENTRYTYPE}")
        return result, self.errors
