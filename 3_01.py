import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

def load_data():
    fname = "Banknote_Authentication.xlsx"
    df = pd.read_excel(fname)
    x_vals = df.iloc[:, :-1].values
    y_vals = df.iloc[:, -1].values
    return x_vals, y_vals

# calculating dot product
def get_dot(a, b):
    v1 = np.array(a)
    v2 = np.array(b)
    return np.dot(v1, v2)

# getting length of vector
def get_len(a):
    v = np.array(a)
    return np.linalg.norm(v)

# finding mean for each class
def get_means(feat, lab):
    cls = np.unique(lab)
    means = {}
    for c in cls:
        # getting rows for this class
        sub = feat[lab == c]
        # mean of class
        means[c] = np.mean(sub, axis=0)
    return means

# finding std dev for each class
def get_spread(feat, lab):
    cls = np.unique(lab)
    stds = {}
    for c in cls:
        # getting rows for this class
        sub = feat[lab == c]
        # std dev of class
        stds[c] = np.std(sub, axis=0)
    return stds

# distance between means
def dist_means(m1, m2):
    return np.linalg.norm(m1 - m2)

# showing histogram
def show_hist(data, name):
    h = np.histogram(data)
    plt.hist(h, bins=20)
    plt.title(f"Density Pattern:{name}")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()

# finding minkowski distance
def get_mink(f1, f2):
    dists = []
    for p in range(1, 11):
        diff = np.abs(np.array(f1) - np.array(f2))
        d = np.power(np.sum(np.power(diff, p)), 1/p)
        dists.append(d)
    return dists

# plotting the distances
def plot_mink(vals):
    plt.plot(range(1, 11), vals, 'go-', label='Minkowski Distances')
    plt.title("Minkowski Distances vs p")
    plt.ylabel('Distance')
    plt.xlabel('p value')
    plt.legend()
    plt.show()

# splitting the data
def split_data(x, y):
    return train_test_split(x, y, test_size=0.3)

# training knn
def train_knn(x_tr, y_tr, k):
    mod = KNeighborsClassifier(n_neighbors=k)
    mod.fit(x_tr, y_tr)
    return mod

# checking accuracy
def get_acc(mod, x_ts, y_ts):
    return mod.score(x_ts, y_ts)

# predicting with knn
def pred_knn(mod, x_ts):
    return mod.predict(x_ts)

def my_knn(x_tr, y_tr, vec, k):
    dists = []
    # finding distance to all points
    for i in range(len(x_tr)):
        d = np.linalg.norm(x_tr[i] - vec)
        dists.append((d, y_tr[i]))
    # sorting them
    dists.sort(key=lambda x: x[0])
    # picking top k
    top = dists[:k]
    # getting labels
    labs = [l for (d, l) in top]
    if sum(labs) > k/2:
        return 1
    return 0

def my_knn_batch(x_tr, y_tr, x_ts, k):
    preds = []
    for row in x_ts:
        preds.append(my_knn(x_tr, y_tr, row, k))
    return np.array(preds)

def compare_res(p1, p2):
    miss = np.sum(p1 != p2)
    tot = len(p1)
    rate = (tot - miss) / tot
    return miss, rate

def plot_accs(x_tr, y_tr, x_ts, y_ts):
    accs = []
    rng = range(1, 12)
    for k in rng:
        # train model again
        mod = train_knn(x_tr, y_tr, k)
        accs.append(get_acc(mod, x_ts, y_ts))
    plt.figure()
    plt.plot(rng, accs, marker='s', color='green')
    plt.xlabel("k")
    plt.ylabel("Accuracy")
    plt.title("KNN Accuracy vs k")
    plt.xticks(rng)
    plt.show()

def check_perf(mod, x_tr, y_tr, x_ts, y_ts):
    tr_pred = mod.predict(x_tr)
    ts_pred = mod.predict(x_ts)
    tr_acc = accuracy_score(y_tr, tr_pred)
    ts_acc = accuracy_score(y_ts, ts_pred)
    cm_tr = confusion_matrix(y_tr, tr_pred)
    cr_tr = classification_report(y_tr, tr_pred)
    cm_ts = confusion_matrix(y_ts, ts_pred)
    cr_ts = classification_report(y_ts, ts_pred)
    diff = tr_acc - ts_acc
    if tr_acc < 0.60:
        return "Underfit"
    elif diff > 0.10:
        return "Overfit"
    return "Regular"

def my_cm(y_real, y_pr):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for real, pr in zip(y_real, y_pr):
        if real == 1 and pr == 1: tp += 1
        elif real == 0 and pr == 0: tn += 1
        elif real == 0 and pr == 1: fp += 1
        elif real == 1 and pr == 0: fn += 1
    return np.array([[tp, fp], [fn, tp]])

def my_metrics(y_real, y_pr):
    cm = my_cm(y_real, y_pr)
    tn, fp = cm[0]
    fn, tp = cm[1]

    acc = (tp + tn) / (tp + tn + fp + fn)
    prec = 0
    rec = 0
    f1 = 0
    if (tp + fp) > 0:
        prec = tp / (tp + fp)
    if (tp + fn) > 0:
        rec = tp / (tp + fn)
    if (prec + rec) > 0:
        f1 = (2 * prec * rec) / (prec + rec)
    return acc, prec, rec, f1, cm

# calculating inverse
def train_lin(x_tr, y_tr):
    return np.linalg.pinv(x_tr) @ y_tr

def pred_lin(mod, x_ts):
    raw = x_ts @ mod
    preds = []
    for v in raw:
        if v >= 0.5:
            preds.append(1)
        else:
            preds.append(0)
    return np.array(preds)

def comp_models(knn, x_tr, y_tr, x_ts, y_ts):
    p_knn = knn.predict(x_tr)
    acc_knn = knn.score(x_tr, y_tr)
    lin = train_lin(x_tr, y_tr)
    p_lin = pred_lin(lin, x_ts)
    acc_lin = accuracy_score(y_ts, p_lin)
    if acc_knn > acc_lin + 0.05:
        return "KNN is better"
    elif acc_lin > acc_knn + 0.05:
        return "Matrix Inversion is better"
    return "Both models perform similarly"

# loading data
x, y = load_data()

if x is not None:
    print(f"Data Loaded. Shape: {x.shape}")

    # a1
    # vector stuff
    v1, v2 = x[0], x[1]
    print(f"Dot Product: {get_dot(v1, v2):.2f}")
    print(f"Length of Vector 1: {get_len(v1):.2f}")

    # a2
    # class stats
    means = get_means(x, y)
    spreads = get_spread(x, y)
    print("Centroids:", list(means.keys()))
    print("Spread (Class 0):", spreads[0])
    print("Distance between Class 0 & 1:", dist_means(means[0], means[1]))

    # a3
    # plotting density
    show_hist(x[:, 0], "Variance Feature")

    dists = get_mink(v1, v2) # a4 calculating distances
    plot_mink(dists) # a5 plotting them

    # a6
    # splitting data
    x_tr, x_ts, y_tr, y_ts = split_data(x, y)
    print(f"Train Size: {x_tr.shape[0]}, Test Size: {x_ts.shape[0]}")

    # a7 to a9
    k = 3
    mod_knn = train_knn(x_tr, y_tr, k)
    acc_sk = get_acc(mod_knn, x_ts, y_ts)
    print(f"Sklearn KNN Accuracy (k={k}): {acc_sk:.4f}")

    # a10
    # classifying own way
    p_sk = pred_knn(mod_knn, x_ts)
    p_own = my_knn_batch(x_tr, y_tr, x_ts, k)
    miss, rate = compare_res(p_sk, p_own)
    print(f"Match Rate with Sklearn: {rate * 100:.2f}% ({miss} mismatches)")

    # a11
    # accuracy plot
    plot_accs(x_tr, y_tr, x_ts, y_ts)

    # a12
    # checking performance
    stat = check_perf(mod_knn, x_tr, y_tr, x_ts, y_ts)
    print(f"Model Status: {stat}")

    # a13
    # my metrics
    acc, prec, rec, f1, cm = my_metrics(y_ts, p_own)
    print(f"My Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
    print("My Confusion Matrix:\n", cm)

    # a14
    # comparing with matrix inversion
    res = comp_models(mod_knn, x_ts, y_ts, x_tr, y_tr)
    print(f"Conclusion: {res}")