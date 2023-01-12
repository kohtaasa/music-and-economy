import pandas as pd

date_range = pd.date_range(start='2017-01-01', end='2022-12-27', freq='D')
date_list = [i.strftime('%Y-%m-%d') for i in date_range]

appended_data = []

for date in date_list:
    df = pd.read_csv(f'/Users/kohtaasakura/PyDev/grad_thesis/charts_data/us_daily/regional-us-daily-{date}.csv')
    df = df[['uri', 'artist_names', 'track_name', 'streams']]
    df.insert(0, 'date', date)
    appended_data.append(df)

agg_df = pd.concat(appended_data, ignore_index=True)
agg_df.to_pickle('charts_us_daily.pkl')
