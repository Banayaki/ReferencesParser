import bibtexparser as p
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime


bibtex_format = """@online{{{title_key},
    title={title},
    date={date},
    year={year},
    author={{TODO: Author or place or corp here}},
    base={{TODO: Base resource title here}},
    url={url}
}}"""


def make_title_key(title):
    return re.sub(r'[^0-9a-z]', '', title, flags=re.IGNORECASE)


def convert_urls_to_bibtex(file_content: str):
    today = datetime.now().strftime('%d.%m.%Y')
    this_year = datetime.now().strftime('%Y')
    
    bibtex_dict = p.loads(file_content, p.bparser.BibTexParser(ignore_nonstandard_types=False))

    for commentary in bibtex_dict.comments:
        if 'http' in commentary:
            r = requests.get(commentary)
            soup = BeautifulSoup(r.content, 'html.parser')
            title = soup.title.string
            bibtex = bibtex_format.format(
                title_key=make_title_key(title),
                title=title,
                date=today,
                year=this_year,
                url=commentary
            )
            
            file_content = file_content.replace(commentary, bibtex)
    
    return file_content            