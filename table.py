import matplotlib.pyplot as plt
import pandas as pd
import re

data = pd.read_csv('result/knapsack_SA.csv',
                   index_col = None).iloc[:,:-1]
data['best'] = data.iloc[:, 1:].max(axis = 1)
data['file'] = data['file'].apply(lambda name : int(re.findall(r'\d+', name)[0]))
order = list(data.columns)[:-1]
order.insert(2,'best')
data = data[order]

fig, ax = plt.subplots(figsize = (15,15))

fig.patch.set_visible(False)
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText = data.values, 
                 colLabels = data.columns,
                 loc = 'center')

for (i,j),cell in table.get_celld().items():
    if i == 0:
        cell.set_text_props(weight = 'bold')
        cell.set_facecolor('gray')
    if j == 0:
        cell.set_text_props(ha = 'left')

plt.tight_layout()
plt.show()