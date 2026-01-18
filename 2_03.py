import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# loading the file
def load(fname):
    return pd.read_excel(fname, sheet_name='thyroid0387_UCI',usecols="A:AE")
# checking types and exploring
def explore(df):
    clean=df.replace('?',np.nan)
    rep=[]
    for col in clean.columns:
        # converting to numeric
        nums=pd.to_numeric(clean[col],errors='coerce')
        is_num=sum(nums.notna())>0 and sum(nums.notna())>len(clean)*0.5
        u_count=clean[col].nunique()
        miss=sum(clean[col].isnull())
        dtype='unknown'
        enc='none'
        # if not numeric
        if not is_num:
            if u_count<=2:
                dtype='Nominal'
                enc='Binary Mapping'
            else:
                dtype='Nominal'
                enc='One-Hot Encoding'
        # if numeric
        else:
            # removing nans
            vals=nums.dropna()
            if (vals %1 ==0).all():
                dtype='Discrete'
            else:
                dtype='Continuous'
            enc='-'

        rng = "-"
        mn = "-"
        var = "-"
        outs = "-"

        if is_num:
            # using numbers
            vals = nums.dropna()

            # range
            mi = vals.min()
            mx = vals.max()
            rng = f"{mi:.2f} - {mx:.2f}"

            # mean and var
            mn = round(vals.mean(), 4)
            var = round(vals.var(), 4)

            # outliers
            sd = vals.std()
            if sd > 0:
                zs = (vals - vals.mean()) / sd
                outs = (abs(zs) > 3).sum()
            else:
                outs = 0

        # adding to list
        rep.append({
            'Attribute': col,
            'Data Type': dtype,
            'Encoding Scheme': enc,
            'Missing Values': miss,
            'Outliers (Z>3)': outs,
            'Range': rng,
            'Mean': mn,
            'Variance': var
        })

    return pd.DataFrame(rep)

# getting binary vectors
def get_bin(df):

    # copying data
    d_bin = df.copy()
    b_cols = []

    for col in d_bin.columns:
        # dropping nans
        u_vals = set(d_bin[col].dropna().unique())

        # checking f/t
        if u_vals.issubset({'f', 't'}):
            d_bin[col] = d_bin[col].map({'f': 0, 't': 1})
            b_cols.append(col)
        # checking f/m
        elif u_vals.issubset({'F', 'M'}):
            d_bin[col] = d_bin[col].map({'F': 0, 'M': 1})
            b_cols.append(col)
        # check 0/1
        elif u_vals.issubset({0, 1}):
            b_cols.append(col)


    v1 = d_bin.iloc[0][b_cols].values
    v2 = d_bin.iloc[1][b_cols].values

    return v1, v2
# calculating jc and smc
def calc_sim(v1, v2):
    # safe check
    f11 = np.sum((v1 == 1) & (v2 == 1))# 1 and 1
    f00 = np.sum((v1 == 0) & (v2 == 0))# 0 and 0
    f01 = np.sum((v1 == 1) & (v2 == 0))# 1 and 0
    f10 = np.sum((v1 == 0) & (v2 == 1))# 0 and 1

    # jaccard math
    denom_j = f11 + f01 + f10
    jc = f11 / denom_j if denom_j != 0 else 0.0

    # smc math
    denom_s = f00 + f01 + f10 + f11
    smc = (f11 + f00) / denom_s if denom_s != 0 else 0.0
    return jc, smc

# calculates cosine
def calc_cos(v1, v2):
    dot = np.dot(v1, v2)
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)

    # return 0 if zero
    if n1 == 0 or n2 == 0:
        return 0.0

    return dot / (n1 * n2)
# plots 3 heatmaps
def plot_heat(df):

    # taking first 20
    sub = df.head(20).copy()

    # binary matrices
    b_sub = sub.copy()
    b_cols = []

    for col in b_sub.columns:
        u_vals = set(b_sub[col].dropna().unique())
        # maps f/t to 0/1
        if u_vals.issubset({'f', 't'}):
            b_sub[col] = b_sub[col].map({'f': 0, 't': 1})
            b_cols.append(col)
        elif u_vals.issubset({'F', 'M'}):
            b_sub[col] = b_sub[col].map({'F': 0, 'M': 1})
            b_cols.append(col)

    b_mat = b_sub[b_cols].values

    # numeric matrix
    n_mat = sub.select_dtypes(include=[np.number]).fillna(0).values

    n = 20
    j_mat = np.zeros((n, n))
    s_mat = np.zeros((n, n))
    c_mat = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            # jc and smc use binary
            jc, smc = calc_sim(b_mat[i], b_mat[j])
            j_mat[i, j] = jc
            s_mat[i, j] = smc

            # cosine uses numeric
            cos = calc_cos(n_mat[i], n_mat[j])
            c_mat[i, j] = cos

    # plotting heatmaps
    fig, ax = plt.subplots(1, 3, figsize=(18, 5))
    # heatmap for jc
    sns.heatmap(j_mat, annot=False, cmap='YlGnBu', ax=ax[0])
    ax[0].set_title('Jaccard Coefficient (Binary)')
    # heatmap for smc
    sns.heatmap(s_mat, annot=False, cmap='YlGnBu', ax=ax[1])
    ax[1].set_title('Simple Matching Coeff (Binary)')
    # heatmap for cosine
    sns.heatmap(c_mat, annot=False, cmap='coolwarm', ax=ax[2])
    ax[2].set_title('Cosine Similarity (Numeric)')

    plt.tight_layout()
    plt.show()

# filling missing stuff
def fill_miss(df):

    clean = df.copy()
    # replace q mark
    clean.replace('?', np.nan, inplace=True)

    for col in clean.columns:
        # skipping empty
        if clean[col].isnull().sum() == 0:
            continue

        if clean[col].dtype == 'object':
            mode = clean[col].mode()[0]
            clean[col] = clean[col].fillna(mode)
        else:
            m = clean[col].mean()
            sd = clean[col].std()
            mx = clean[col].max()

            # if constant just use mean
            if sd == 0:
                clean[col] = clean[col].fillna(m)
                continue
            # check outliers
            z = (mx - m) / sd

            if abs(z) > 3:
                med = clean[col].median()
                clean[col] = clean[col].fillna(med)
            else:
                clean[col] = clean[col].fillna(m)

    return clean

# normalizing data
def norm_data(df):
    nums = df.select_dtypes(include=[np.number])
    # doing min max
    norm = (nums - nums.min()) / (nums.max() - nums.min())
    return norm

fname = 'Lab Session Data.xlsx'

# loading
data = load(fname)
# a4
res = explore(data)
print(res.to_string(index=False))
# a5
# calc similarity
v1, v2 = get_bin(data)
jc, smc = calc_sim(v1, v2)# calculates both
print(f"Jaccard Coefficient (Binary): {jc:.4f}")
print(f"Simple Matching Coeff (Binary): {smc:.4f}")

# a6
# calc cosine
num_df = data.select_dtypes(include=[np.number]).fillna(0)
v1_n = num_df.iloc[0].values
v2_n = num_df.iloc[1].values
cos = calc_cos(v1_n, v2_n)
print(f"Cosine Similarity (Numeric): {cos:.4f}")

# a7
# plotting heatmaps
plot_heat(data)

# a8
# imputing values
# check before
miss1 = data.replace('?', np.nan).isnull().sum().sum()
print(f"Total missing values before: {miss1}")

clean = fill_miss(data)

# check after
miss2 = clean.isnull().sum().sum()
print(f"Total missing values after:  {miss2}")

# a9
# normalize
n_df = norm_data(clean)

# show sample
print("Sample of Normalized Data (First 5 rows, Age column):")
# assuming age is numeric
if not n_df.empty:
    fst = n_df.columns[0]
    print(n_df[fst].head())
else:
    print("No numeric data found to normalize.")