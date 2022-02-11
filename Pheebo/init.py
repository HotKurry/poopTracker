import pandas as pd

df2 = pd.DataFrame([

],
  columns=[ 'Post ID', 'Date', 'Post Type', 'reply' ])

df2.to_csv('Elontracker.csv')

print(df2)

df = pd.read_csv('Elontracker.csv', index_col=0)
print(df)
