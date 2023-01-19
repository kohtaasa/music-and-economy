import pandas as pd

df = pd.read_pickle('billboard_audio_features_1960.pkl')
print(df.info())
print(df.head())

