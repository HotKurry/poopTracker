import pandas as pd
import os

homeFolder= os.getcwd()

df2 = pd.DataFrame([

],
  columns=[ 'Post ID', 'Date', 'Post Type', 'reply' ])

df2.to_csv(homeFolder + 'Elontracker.csv')

print(df2)

df = pd.read_csv(homeFolder + 'Elontracker.csv', index_col=0)
print(df)

print(os.getcwd())