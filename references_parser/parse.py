import argparse
from .Parser import Parser
from .IeeeParser import IEEEParser

PARSER_MAPPING = {
    'itnt': Parser(),
    'ieee': IEEEParser()
}

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('path', type=str,
                           help='Path to the file containing bibtext citations.')
    argparser.add_argument('-s', '--save', type=str,
                           help='Path to file where to save the result of parsing.', default='')
    argparser.add_argument('-p', '--parser', type=str,
                           help='Parser to use. Available parsers: ieee, itnt. Default: itnt.', default='itnt')

    args = argparser.parse_args()
    with open(args.path, 'r') as f:
        citations = f.read()

    parser_type = args.parser.lower()
    parser = PARSER_MAPPING.get(parser_type)
    if parser is None:
        raise ValueError(f"Unknown parser type. Expect one of {list(PARSER_MAPPING.keys())}, but received"
                         f"{parser_type}")

    result = parser(citations)
    for entry in result:
        print(entry, end="\n\n")

    if args.save != '':
        with open(args.save, 'w', encoding='utf-8') as f:
            for entry in result:
                f.write(entry + '\n\n')
        print(f'Saved result to {args.save}.')
