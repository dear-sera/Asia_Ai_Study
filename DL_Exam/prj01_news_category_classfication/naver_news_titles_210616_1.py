import pandas as pd

fi = pd.read_csv('./crawling_data/1-100.csv')
se = pd.read_csv('./crawling_data/101-200.csv')
th = pd.read_csv('./crawling_data/201-300.csv')
fo = pd.read_csv('./crawling_data/301-422.csv')

final = pd.concat([fi, se, th, fo], ignore_index=True)

print(final.shape)

final.to_csv('./crawling_data/Econimic_crawling.csv', index=False)