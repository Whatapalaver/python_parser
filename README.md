# Python Parser

## Run the Parser

- With a single file output for use as histogram input: `python parser/parse.py -j data_all/ -o dumps/`
- For multi-file output: `python parser/parse.py -j data_all/ -o dumps/ -m`

## Run the Histogram Generator

- Run all available fields with defaults set: `python analysis/hist.py`
- Specific field histogram with max y-axis = 750 and bucke size of 20: `python analysis/hist.py -f physicalDescription -m 750 -b 20`
- To generate a full scale insetted subplot for the title field `python analysis/hist.py -f title -m 250 -b 10 -i dumps/output.csv -s`

## TODO

### Parser

- [ ] Refactor
- [ ] Better handling of extract objects and csv writing loop. Use `extract_objects(args)` again

#### Parser Input

- [ ] Currently deals with json_input only, amend to accept API calls as well as files
- [ ] Uses os.walk to process files in directory - amend to allow single file processing
- [x] Want to amend output option to single or multiple files

#### Parser Data Processing

- [ ] currently only working with the flat data - need to prepare the nested data extraction

#### Parser Output

- [ ] Make sure the process overwrites output file on the initial run
- [ ] Need to sort header generation for single file parser - hard coded currently

### Histogram generator

- [ ] Refactor

#### Hist Input

- [x] implement argparse
- [x] specify input file
- [x] allow override of bin size
- [x] allow override of max axis
- [x] allow to process single field type
- [ ] Pandas to deal with multiple files. Currently have a section of parser that outputs individual named processed files, this is commented out as I haven't fathomed how to get pandas to process multiple inputs
