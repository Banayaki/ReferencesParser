# Install

```bash
pip install references-parser
```
# Usage

There are 2 ways of using parser:
1. Write a Python script (or Jupyter Notebook) and do parsing manually using the library.
2. Do parsing from terminal. The steps are as follows:
   1. Put bibtex citations in a text file `filename.txt`.
   2. Open terminal in the corresponding folder.
   3. Enter the command `python -m references_parser.parse filename.txt -s parse_result.txt`. 
   You may change the parser type via `-p` parameter. Available parsers: ssau, ieee.
   4. Parsing results will be saved in `parse_result.txt`.

# Examples

Follow `examples` folder to see input and outputs file examples

# Contribution
If you want to improve the program - just fork it and make a pool request
