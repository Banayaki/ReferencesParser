from typing import Optional, Tuple

import bibtexparser as p

from .bibtex import Bibtex


class BibtexSsau(Bibtex):
    def get_parsed_authors(
        self, return_all=False, space_between_initials=False
    ) -> Tuple[Optional[str], str]:
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

        last_names_joiner = "-"  # "" was used previously
        initials_joiner = " " if space_between_initials else ""
        authors_joiner = ", "

        def merged_last_names(splitted_author):
            return last_names_joiner.join(splitted_author["last"])

        def all_first_name_initials(splitted_author):
            return initials_joiner.join(
                [f"{first_name[0]}." for first_name in splitted_author["first"]]
            )

        def parse_single_author(str_author):
            splitted_author = p.customization.splitname(str_author)
            return (
                all_first_name_initials(splitted_author)
                + " "
                + merged_last_names(splitted_author)
            )

        splitted_first_author = p.customization.splitname(author_string[0])
        first_author = (
            merged_last_names(splitted_first_author)
            + ", "
            + all_first_name_initials(splitted_first_author)
        )

        if len(author_string) < 4 or return_all:
            authors = authors_joiner.join(
                [parse_single_author(str_author) for str_author in author_string]
            )
        elif len(author_string) == 4:
            authors = authors_joiner.join(
                [parse_single_author(str_author) for str_author in author_string]
            )
            first_author = None
        else:
            authors = authors_joiner.join(
                [parse_single_author(str_author) for str_author in author_string[:3]]
            )
            first_author = None
            authors = f"{authors} [и др.]"
        return first_author, authors
