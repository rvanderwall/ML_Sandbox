import bnlearn
import pandas as pd
from scipy.stats import hypergeom

"""
https://towardsdatascience.com/a-step-by-step-guide-in-detecting-causal-relationships-using-bayesian-structure-learning-in-python-c20c6b31cee5
"""

def run_titanic():
    # Load titanic dataset
    df = bnlearn.import_example(data='titanic')

    print(df[['Survived', 'Sex']])
    #     Survived     Sex
    #0           0    male
    #1           1  female
    #2           1  female
    #3           1  female
    #4           0    male
    #..        ...     ...
    #886         0    male
    #887         1  female
    #888         0  female
    #889         1    male
    #890         0    male
    #[891 rows x 2 columns]

    # Total number of samples
    N = df.shape[0]
    # Number of success in the population
    K = sum(df['Survived'] == 1)
    # Sample size/number of draws
    n = sum(df['Sex'] == 'female')
    # Overlap between female and survived
    x = sum((df['Sex'] == 'female') & (df['Survived'] == 1))

    print(x-1, N, n, K)
    # 232 891 314 342

    # Compute
    P = hypergeom.sf(x, N, n, K)
    P = hypergeom.sf(232, 891, 314, 342)

    print(P)