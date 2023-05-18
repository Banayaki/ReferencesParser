# Install

```bash
pip install references-parser
```
# Usage

### Use help to see CLI parameters
```bash
➜ python -m references_parser parse --help        
Usage: python -m references_parser parse [OPTIONS] PATH

Options:
  -s, --save TEXT         Path to file where to save the result of parsing.
  -p, --parser TEXT       Parser to use. Available parsers: ieee, ssau.
                          Default: ssau.
  -v, --verbose           Whether to print output to stdout or not
  -b, --beautify INTEGER  Number of line wraps between references. Default: 1
  --help                  Show this message and exit.
```

### Usual way of using the script
```bash
python -m references_parser parse in.txt
```

# Website references

It's hard to fully parse a website automatically, so some manual interactions are required.

How to add a website reference:

1. Add the links directly to the input file.
2. Invoke the `prepare-urls` command like this:

```bash
python -m references_parser prepare-urls in.txt
```

3. Then, the URL in the file will be replaced with a BibTeX-annotated URL:

```
@online{Google,
    title={Google},
    date={18.05.2023},
    year={2023},
    origin={TODO: Author or place or corp here},
    base={TODO: Base resource title here},
    url={<https://google.com>}
}
```

4. Here, you can fill in the fields `origin` **(mandatory)** and `base` with the required information.
5. Then, you can use parsers as usual, but pay attention that the result contains `[Б.м.]`, which you may want to delete.


# Examples

Follow `examples` folder to see input and outputs file examples

# Contribution
If you want to improve the program - just fork it and make a pool request
