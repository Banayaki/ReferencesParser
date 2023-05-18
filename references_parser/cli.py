import click
from .converters.url_converter import convert_urls_to_bibtex
from .parsers import SsauParser
from .parsers import IEEEParser


PARSER_MAPPING = {
    'ssau': SsauParser(),
    'ieee': IEEEParser(),

}


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', type=str)
@click.option('-s', '--save', type=str, help='Path to file where to save the result of parsing.', default='')
@click.option('-p', '--parser', type=str, help='Parser to use. Available parsers: ieee, ssau. Default: ssau.', default='ssau')
def parse(path: str, save: str, parser: str, *args, **kwargs):
    with open(path, 'r', encoding='utf-8') as f:
        citations = f.read()

    parser_type = parser.lower()
    parser = PARSER_MAPPING.get(parser_type)
    if parser is None:
        raise ValueError(f"Unknown parser type. Expect one of {list(PARSER_MAPPING.keys())}, but received"
                         f"{parser_type}")

    result = parser(citations)
    for entry in result:
        print(entry, end="\n\n")

    if save:
        with open(save, 'w', encoding='utf-8') as f:
            for entry in result:
                f.write(entry + '\n\n')
        print(f'Saved result to {save}.')


@cli.command()
@click.argument('path', type=str)
def prepare_urls(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        citations = f.read()
        
    citations = convert_urls_to_bibtex(citations)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(citations)
        
        
if __name__ == '__main__':
    cli()  
