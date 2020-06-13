# Fuzzy Matcher

## Why Fuzzy Matcher?

Table operations are one of the fundamental operations in data science and analytics. Whether it be merging of two tables based on common columns or producing a data mapping using many datasets, table operations are necessary. Unfortunately, not all the datasets are clean with uniform names and spellings, even more so when data is manually produced. 

Fuzzy Matcher helps to merge the tables even when the common columns have different spellings. Using [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance), the similar spellings can be mapped to one another. We use [SeatGeek](https://github.com/seatgeek)'s [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) Python package to perform the fuzzy matching.

## Requirement

This script requires Python (Version 3.4+) to be installed on the system. Though Python packages like [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) and [pandas](https://pandas.pydata.org/) are used in this script, they will be self-installed if the script does not find them on the system.

Download Python from [here](https://www.python.org/downloads/).

## Usage
Download the whole repository or just the [fuzzy.py](fuzzy.py) file and run the following command in terminal or command-line prompt. Note that you need to be in the same path as the [fuzzy.py](fuzzy.py) file is in.


```
python fuzzy.py [-h] --firstcsv FIRSTCSV --secondcsv SECONDCSV
                [--destination DESTINATION] --commoncolumns1 COMMONCOLUMNS1
                --commoncolumns2 COMMONCOLUMNS2 [--in {second,first}]

Arguments:
  -h, --help            show this help message and exit
  --firstcsv FIRSTCSV   CSV file for first table.
  --secondcsv SECONDCSV
                        CSV file for second table.
  --destination DESTINATION
                        Destination filename.
  --commoncolumns1 COMMONCOLUMNS1
                        Common columns for first table.
  --commoncolumns2 COMMONCOLUMNS2
                        Common columns for second table in the same order.
  --in {second,first}   Table to append the columns.


Optional arguments:
  --destination DESTINATION
                        Defaults to output.csv
  --in                  Defaults to second.

Format for arguments:
  --firstcsv FIRSTCSV   Filename with .csv extension (example: abc.csv).
  --secondcsv SECONDCSV Filename with .csv extension (example: xyz.csv)
  --destination DESTINATION
                        Filename with .csv extension (example: output.csv)
  --commoncolumns1 COMMONCOLUMNS1
                        Comma-separated common columns of the first table
                        enclosed by quotes (example: 'District,Local Unit,Ward')
  --commoncolumns1 COMMONCOLUMNS1
                        Comma-separated common columns of the second table
                        enclosed by quotes (example: 'Jilla,Palika,Ward Number'
  --in                  Takes either 'second' or 'first'. Other argument would be invalid. 

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgement
Nepal Poverty Team, The World Bank, Nepal Country Office 