import pandas as pd
import numpy as np
import time

import sys, argparse


# read file name from cmd param
parser = argparse.ArgumentParser()

parser.add_argument("Input", help = "Pass in a file.")
parser.add_argument( "-o", "--Output", 
                     help = "Save result to file. A file name is optional.", 
                     nargs= '?', const= f'Output-{time.time()}.csv')

args = parser.parse_args()

# file names
in_file = args.Input
out_file = args.Output


# read in file
df = pd.read_csv(in_file, header= None)

# remove file name row
orig_header, df = df.iloc[:2], df.iloc[2:]


# organize df header and index
df.reset_index(drop= True, inplace= True)
df.rename(columns= {0:'Heading', 1:'Item', 2:'Value'}, inplace= True)

# split by heading
df['Heading'].fillna('', inplace= True)
heading_idx = df.loc[df['Heading'].str.contains('Heading')].index

splits = []
for idx, sect  in enumerate(heading_idx):
    try:
        temp = df.iloc[sect: heading_idx[idx + 1]].copy()

    except:
        temp = df.iloc[sect: ].copy()

    # add total
    temp.reset_index(drop= True, inplace= True)
    total = temp['Value'].sum()
    temp.loc[len(temp.index)] = ['', 'Sub Total', total]

    splits.append(temp)

# merge all sections
sects_df = pd.concat(splits)


# add gross total
sects_df.reset_index(drop= True, inplace= True)
gross_total = sects_df.loc[sects_df['Item'] == 'Sub Total']['Value'].sum()
sects_df.loc[len(sects_df)] = ['', 'Total', gross_total]

# outputs
sects_df.rename(columns= {'Heading':0, 'Item':1, 'Value': 2}, inplace= True)
df = pd.concat([orig_header, sects_df])

df.to_csv(out_file, index= False, header= False) if(out_file)else(None)
print(sects_df)
