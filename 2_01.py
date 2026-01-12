import numpy as np
import pandas as pd
def read_data(filename):
     df = pd.read_excel(filename)
     df.dropna(how="all", axis=1, inplace=True)
     selected_data = df[["Candies (#)","Mangoes (Kg)","Milk Packets (#)"]]
     X = selected_data.values.tolist()
     selected_output = df["Payment (Rs)"]
     y = selected_output.values.tolist()
     rank = np.linalg.matrix_rank(X)
     pinv = np.linalg.pinv(X)
     return X,y,rank,pinv

filename = 'Lab Session Data.xlsx'
X_in,y_in,rank_X,pinv_X = read_data(filename)
print(f"{X_in}\n",y_in,f"\nThe rank of the matrix is {rank_X}",f"\nThe pinv of X is {pinv_X}")

