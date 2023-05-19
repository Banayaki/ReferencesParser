from typing import Optional, Tuple

import bibtexparser as p

from .bibtex import Bibtex


class BibtexSsau(Bibtex):
    def get_parsed_authors(self, return_all=False) -> Tuple[Optional[str], str]:
        """
        Perform authors entry parsing using following rules:
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

        Returns:
            Tuple[Optional[str], str]: first author and others
        """
        author_string = self.author

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
