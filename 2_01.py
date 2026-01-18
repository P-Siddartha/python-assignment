from operator import index

import numpy as np
import pandas as pd
# loading the data
def load(fname):
    return pd.read_excel(fname,usecols='A:E')
# getting features and output
def get_data(df):
    sel=df[['Candies (#)','Mangoes (Kg)','Milk Packets (#)']]
    x=sel.values.tolist()
    out=df['Payment (Rs)']
    y=out.values.tolist()
    return np.array(x),np.array(y)
# finding the rank
def get_rank(mat):
    f_mat=np.array(mat)
    return np.linalg.matrix_rank(f_mat)
# finding cost with inverse
def get_cost(feats,out):
    inv=np.linalg.pinv(feats)
    ans=inv @ out
    return list(ans.round(2))
# checking if rich or poor
def classify(val):
    if val>200:
        return "RICH"
    else:
        return "POOR"
# a1
# loading data to df
fpath = 'Lab Session Data.xlsx'
df = load(fpath)

# getting vectors
mat_x, vec_y = get_data(df)

# calculate rank
r = get_rank(mat_x)
print(f"Dimensionality (Rank) of the vector space: {r}")

# calculate cost
c = get_cost(mat_x, vec_y)
print(f"Cost of Candies, Mangoes, Milk: {c}")

# classifying rich poor
# using function on payment col
df['Category'] = df['Payment (Rs)'].apply(classify)

# a2
# showing results
print(df[['Customer','Payment (Rs)', 'Category']].to_string(index=False))