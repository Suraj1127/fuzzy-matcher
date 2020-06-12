#!/usr/bin/env python3

"""
Description: Python script to append the common columns in one sheet from another sheet using fuzzy matching.
"""
import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])  
        
import os
import sys
import argparse

import_or_install('numpy')
import_or_install('pandas')
import_or_install('fuzzywuzzy')

import numpy as np
import pandas as pd
from fuzzywuzzy import process, fuzz


class FuzzyMatcher:
    """
    FuzzyMatcher class to perform the fuzzy matching.
    """
    
    def __init__(self, df_1, df_2, columns_1, columns_2, append_in='second'):
        """
        The constructor takes five arguments. The last argument 'append_in' is optional.
        
        Parameters:
        df_1: the first table in pandas.DataFrame format or the name of the CSV file for the first table
        df_2: the second table in pandas.DataFrame format or the name of the CSV file for the second table
        columns_1: list of common columns in the first table
        columns_2: list of common columns in the second table
        append_in (optional): 
            'first' if the common columns are to be appended in the first table
            'second' if the common columns are to be appended in the second table
        """
        
        if type(df_1) == str:
            df_1 = pd.read_csv(df_1)
            
        if type(df_2) == str:
            df_2 = pd.read_csv(df_2)
            
        df_1.columns = df_1.columns.str.lower().str.strip()
        df_2.columns = df_2.columns.str.lower().str.strip()
        
        if append_in == 'first':
            
            temp = df_1
            df_1 = df_2
            df_2 = temp
            
            temp = columns_1
            columns_1 = columns_2
            columns_2 = temp
        
        self.df_1 = df_1.rename(columns=dict(zip(columns_1, columns_2)))
        
        self.columns = columns_2
        
        df_1.columns = df_1.columns.str.lower().str.strip()
        df_2.columns = df_2.columns.str.lower().str.strip()
        
        self.df_2 = self._fuzzy_match(self.df_1, df_2, self.columns[0])
        
        
    @staticmethod
    def _string_matching(name, collection, mapping_={}):
        """
        Returns similar name using fuzzy matching.
        """
        if name in collection:
            return name

        if name in mapping_:
            return mapping_[name]

        similar = process.extractOne(name, collection, scorer=fuzz.ratio)[0]
        mapping_[name] = similar

        return similar
    
    
    def _fuzzy_match(self, df_1_t, df_2_t, common_column_t):
        """
        Returns dataframe with the common column appended.
        
        Notice that the appended columns end with '_t'.
        """
        collection = set(df_1_t[common_column_t])
        
        df_2_t[common_column_t + '_t'] = df_2_t[common_column_t].apply(self._string_matching, args=(collection,))
        
        return df_2_t
    
    
    @property
    def fuzzy_match(self):
        """
        Returns the dataframe consisting of all the appended columns.
        """
        for i_t, common_column in enumerate(self.columns[1:], start=1):
            
            self.df_2[common_column + '_t'] = np.nan
            
            collection = set(self.df_1[common_column])
            
            group_1 = self.df_1.groupby(self.columns[:i_t])
            
            group_2 = self.df_2.groupby([i + '_t' for i in self.columns[:i_t]])
            
            for key, df_slice_2 in group_2:
                
                df_slice_1 = group_1.get_group(key)
                
                df_slice_2 = self._fuzzy_match(df_slice_1, df_slice_2, common_column)
                
                self.df_2.loc[df_slice_2.index, common_column + '_t'] = df_slice_2.loc[:, common_column + '_t']

        return self.df_2 
    
    
    def save(self, filename):
        """
        Saves the result dataframe to a CSV file, filename.
        """
        self.df_2.to_csv(filename)


def parse_args(parser):
    """
    Parsing and configuration of the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--firstcsv', type=str, required=True, help='CSV file for first table.')
    parser.add_argument('--secondcsv', type=str, required=True, help='CSV file for second table.')

    parser.add_argument('--destination', type=str, default='output.csv', help='Destination filename.')
    parser.add_argument('--commoncolumns1', type=str, required=True, help='Common columns for first table.')
    parser.add_argument('--commoncolumns2', type=str, required=True, help='Common columns for second table in the same order.')
    parser.add_argument("--in", dest="_in", default='second', choices=['second', 'first'], help='Table to append the columns. ')
    return check_args(parser.parse_args())


def check_args(args):
    """
    Checking the arguments if they are entered properly.
    
    Validations performed:
        1. Compulsory arguments are entered.
        2. The entered filenames are present in the current folder.
        3. The entered column names are present in the corresponding files.
        4. If the destination filename is already present in the directory, ask the user if it can be overwritten.
    """
    
    # for --firstcsv and --secondcsv
    for filename in [args.firstcsv, args.secondcsv]:
        if not os.path.isfile(filename):
            raise Exception("File {} is not present in the currrent folder.".format(filename))

    # --commoncolumns1
    commoncolumns1 = [i.strip().lower() for i in args.commoncolumns1.split(',')]
    temp = set(commoncolumns1) - set(pd.read_csv(args.firstcsv, nrows=1).columns.str.lower().str.strip())
    if temp:
        raise Exception("The following columns are not present in the file, {}:\n{}".format(args.firstcsv, temp))
    
    # --commoncolumns2
    commoncolumns2 = [i.strip().lower() for i in args.commoncolumns2.split(',')]
    temp = set(commoncolumns2) - set(pd.read_csv(args.secondcsv, nrows=1).columns.str.lower().str.strip())
    if temp:
        raise Exception("The following columns are not present in the file, {}:\n{}".format(args.secondcsv, temp))
    
    # --destination
    if os.path.isfile(args.destination):
        print("The file {} already exists. Do you want to overwrite it? y/n".format(args.destination))
        ans = input().strip().lower()
        
        if ans == 'n':
            print("Please enter different destination filename and run the script again.")
            sys.exit()
            
    return args


if __name__ == "__main__":
    
    # instantiate the ArgumentParser class and parse the arguments
    parser = argparse.ArgumentParser()
    arguments = parse_args(parser)
    
    # save the arguments as some variables which later would be passed to FuzzyMatcher class
    filename_1 = arguments.firstcsv
    filename_2 = arguments.secondcsv
    
    result_filename = arguments.destination
    
    # clean and lowercase-ize the columns names
    common_columns_1 = [i.strip().lower() for i in arguments.commoncolumns1.split(',')]
    common_columns_2 = [i.strip().lower() for i in arguments.commoncolumns2.split(',')]
    
    # instantiate the FuzzyMatcher object, perform the fuzzy match, and save the result to the destination CSV file
    fuzzy_matcher = FuzzyMatcher(filename_1, filename_2, common_columns_1, common_columns_2, append_in=arguments._in)
    fuzzy_matcher.fuzzy_match
    fuzzy_matcher.save(result_filename)
    
    
    