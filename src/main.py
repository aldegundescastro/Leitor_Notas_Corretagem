import pandas as pd
import numpy as np
from scipy import stats
from glob import glob

# Lendo aquivos
#path = 'btcusdt_2018_backtest_sem_sobreposicao_de_orders.csv'
#df = pd.read_csv(path, delimiter=';')

files = sorted(glob(r'./data/btcusdt_tendencia/*.xlsx'))
df = pd.concat((pd.read_excel(cont) for cont in files),ignore_index=True)

#df['profit']=df['profit'].str.replace(',', '.')
df['profit']=df['profit'].astype(float)
#df['cumulative_profit']=df['cumulative_profit'].str.replace(',', '.')
#df['cumulative_profit']=df['cumulative_profit'].astype(float)
df['cumulative_profit'] = df['profit'].cumsum()
print(files)