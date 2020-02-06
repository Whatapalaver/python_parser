# Python Parser

## To Run the Parser

- With a single file output for use as histogram input: `python parser/parse.py -j data_all/ -o dumps/`
- For multi-file output: `python parser/parse.py -j data_all/ -o dumps/ -m`

## To Run the Histogram Generator

- Run all available fields with defaults set: `python analysis/hist.py`
- Specific field histogram with max y-axis = 750 and bucke size of 20: `python analysis/hist.py -f physicalDescription -m 750 -b 20`

## TODO

### Input Options for parse.py

- [ ] Currently deals with json_input only, amend to accept API calls as well as files
- [ ] Uses os.walk to process files in directory - amend to allow single file processing
- [x] Want to amend output option to single or multiple files

### Input options for hist.py

- [x] implement argparse
- [x] specify input file
- [x] allow override of bin size
- [x] allow override of max axis
- [x] allow to process single field type

### Data to process

- [ ] currently only working with the flat data - need to prepare the nested data extraction

### Output Options

- [ ] Pandas to deal with multiple files. Currently have a section of parser that outputs individual named processed files, this is commented out as I haven't fathomed how to get pandas to process multiple inputs
- [ ] Make sure the process overwrites output file on the initial run
