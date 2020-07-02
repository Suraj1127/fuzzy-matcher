# Fuzzy Matcher

## Why Fuzzy Matcher?

Table operations are one of the fundamental operations in data science and analytics. Whether it be merging of two tables based on common columns or producing a data mapping using many datasets, table operations are necessary. Unfortunately, not all the datasets are clean with uniform names and spellings, even more so when data is manually produced. 

Fuzzy Matcher helps to merge the tables even when the common columns have different spellings. Using [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance), the similar spellings can be mapped to one another. We use [SeatGeek](https://github.com/seatgeek)'s [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) Python package to perform the fuzzy matching.

## Requirements

This script requires Python (Version 3.4+) to be installed on the system. Though Python packages like [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) and [pandas](https://pandas.pydata.org/) are used in this script, they will be self-installed if the script does not find them on the system. Make sure you have latest version of pip installed in your system.

Download Python from [here](https://www.python.org/downloads/).

## Usage

### General Use

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

### Developers Use
Developers can use the `FuzzyMatcher` class and integrate the fuzzy spelling matching functionality on their script. 

While instantiating the class, it takes five arguments (with one argument being _optional_). 

#### Instance parameters
```
Parameters:
        df_1: the first table in pandas.DataFrame format or the name of the CSV file for the first table
        df_2: the second table in pandas.DataFrame format or the name of the CSV file for the second table
        columns_1: list of common columns in the first table
        columns_2: list of common columns in the second table
        append_in (optional): 
            'first' if the common columns are to be appended in the first table
            'second' if the common columns are to be appended in the second table
```
Example:
```
fuzzy_matcher = FuzzyMatcher('economies.csv', 'countries.csv', ['Continent', 'Economy'], ['Cont', 'Country'], append_in='first')
```

#### Fuzzy matching
After instantiating the class, the matching can be done easily by calling the `fuzzy_match` property. It returns the result in pandas DataFrame format with the columns appended.

Example:
```
df = fuzzy_matcher.fuzzy_match
```
#### Saving
After making the matching, the result can be easily exported to _CSV_ format using `save` method of the class.

Example:
```
fuzzy_matcher.save('output.csv')
```
 
## Admin Codes
Central Bureau of Statistics (CBS) codes, High Level Commission for Information and Technology (HLCIT) codes and P-codes (used by UN agencies like UN-OCHA) for all the new districts (total of 77) and palikas (local units) are compiled and provided in the CSV format under the filename, _admin_codes.csv_. For designated areas like national parks and wildlife reserves, the CBS codes are not available, so the fields are left empty.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgement
Nepal Poverty Team, The World Bank, Nepal Country Office 

---
Contact email: _regmi125@gmail.com_