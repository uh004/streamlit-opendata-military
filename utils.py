import pandas as pd

def load_data():
  data = pd.read_csv('soldier.csv')
  return data