import click

from .converters.url_converter import convert_urls_to_bibtex
from .parsers import IEEEParser, SsauParser

PARSER_MAPPING = {
    "ssau": SsauParser(),
    "ieee": IEEEParser(),
    # 'ieee': IEEEParser(),
}


def log_errors(errors):
    if errors is not None and len(errors.keys()) > 0:
        print("Some errors was occured during parsing:")
        for bibtex_title, error in errors.items():
            for k, v in error.items():
                print(f"ERROR | {bibtex_title}: {k} - {v}")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("path", type=str)
@click.option(
    "-s",
    "--save",
    type=str,
    help="Path to file where to save the result of parsing.",
    default="",
)
@click.option(
    "-p",
    "--parser",
    type=str,
    help="Parser to use. Available parsers: ieee, ssau. Default: ssau.",
    default="ssau",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Whether to print output to stdout or not",
    default=False,
)
@click.option(
    "-b",
    "--beautify",
    type=int,
    help="Number of line wraps between references. Default: 1",
    default=1,
)
def parse(path: str, save: str, parser: str, verbose: bool, beautify: int):
    with open(path, "r", encoding="utf-8") as f:
        citations = f.read()

    parser_type = parser.lower()
    parser = PARSER_MAPPING.get(parser_type)
    if parser is None:
        raise ValueError(
            "Unknown parser type. Expect one of " +
            f"{list(PARSER_MAPPING.keys())}, but received"
            f"{parser_type}"
        )

    result, errors = parser(citations)

    end = "".join(["\n" for _ in range(beautify)])

    if verbose:
        for entry in result:
            if entry is not None:
                print(entry, end=end)

    if save:
        with open(save, "w", encoding="utf-8") as f:
            for entry in result:
                if entry is not None:
                    f.write(entry + end)
        print(f"Saved result to {save}.")

    log_errors(errors)


@cli.command()
@click.argument("path", type=str)
def prepare_urls(path: str):
    with open(path, "r", encoding="utf-8") as f:
        citations = f.read()

    citations, errors = convert_urls_to_bibtex(citations)

    with open(path, "w", encoding="utf-8") as f:
        f.write(citations)

    log_errors(errors)


if __name__ == "__main__":
    cli()
