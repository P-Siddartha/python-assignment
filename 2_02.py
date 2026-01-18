import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# loading the file
def load(fname):
    return pd.read_excel(fname,sheet_name="IRCTC Stock Price",usecols='A:I')

def calc_stats(df):
    col=df['Price']
    x=np.array(col.values)
    return x.mean(),x.var()

def my_stats(df):
    col=df['Price']
    total=col.values.sum()
    n=col.shape[0]
    m=total/n
    obs=pow(col.values-m,2)
    v=obs.sum()/n
    return m,v

def check_acc(m1,v1,m2,v2):
    if np.isclose(m1,m2) and np.isclose(v1,v2):
        return True
    else:
        return False

def check_time(df,func):
    t=0
    for i in range(10):
        t1 = time.time()
        func(df)
        t2 = time.time()
        t += t2 - t1
    avg = t/10
    return avg

def wed_mean(df):
    wd=df[df['Day']=='Wed']
    return wd['Price'].mean()

def apr_mean(df):
    ad=df[df['Month']=='Apr']
    return ad['Price'].mean()

def comp_mean(samp,pop):
    if np.isclose(samp,pop):
        return True
    return False

def loss_prob(df):
    clean=df['Chg%'].astype(str).str.replace('%','').astype(float)
    bad=clean.apply(lambda x:x < 0)
    prob=sum(bad)/len(clean)
    return prob

def wed_profit(df):
    wd = df[df['Day'] == 'Wed']
    clean = wd['Chg%'].astype(str).str.replace('%', '').astype(float)
    good = clean.apply(lambda x: x > 0)
    prob = sum(good) / len(df)
    return prob

def cond_profit(df):
    wd=df[df['Day']=='Wed']
    clean=wd['Chg%'].astype(str).str.replace('%','').astype(float)
    good=clean.apply(lambda x:x > 0)
    prob=sum(good)/len(clean)
    return prob

def plot_graph(df):
    p_data=df.copy()
    p_data['val']=p_data['Chg%'].astype(str).str.replace('%','').astype(float)
    days=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    p_data['Day']=p_data['Day'].astype(str).str.strip()
    p_data['Day']=pd.Categorical(p_data['Day'],categories=days,ordered=True)
    p_data=p_data.sort_values(by=['Day'])
    plt.figure(figsize=(10,6))
    plt.scatter(p_data['Day'],p_data['val'],color='green',alpha=0.5)
    plt.title('Scatter plot of Chng data against the Day of the week')
    plt.ylabel('Price change Percentage')
    plt.xlabel('Day of the week')
    plt.grid(True)
    plt.show()

# a3
fname = 'Lab Session Data.xlsx'
data = load(fname)

# mean and variance
pm, pv = calc_stats(data)
om, ov = my_stats(data)
print(f"Package: Mean={pm:.4f}, Var={pv:.4f}")
print(f"Own:     Mean={om:.4f}, Var={ov:.4f}")

if check_acc(om, ov, pm, pv):
        print("Accuracy Check: PASSED")
else:
        print("Accuracy Check: FAILED")

# complexity stuff
print("\n--- Complexity ---")
t1 = check_time(data, calc_stats)
t2 = check_time(data, my_stats)
print(f"Pkg Time: {t1:.6f}s")
print(f"Own Time: {t2:.6f}s")

# specific means
print("\n--- Specific Means ---")
print(f"Wednesday Mean: {wed_mean(data):.4f}")
print(f"April Mean:     {apr_mean(data):.4f}")

# probabilities
p_loss = loss_prob(data)
p_wed = wed_profit(data)
p_cond = cond_profit(data)

print(f"Loss Probability: {p_loss:.4f}")
print(f"Profit on Wed (Joint): {p_wed:.4f}")
print(f"Profit given Wed (Conditional): {p_cond:.4f}")

# plot
plot_graph(data)