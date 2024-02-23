import pandas as pd
import requests
pd.set_option("display.max_columns", None)
import time
import numpy as np

test_url = "https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=2012-13&SeasonType=Regular%20Season&StatCategory=PTS"
r = requests.get(url=test_url).json()
table_headers = r["resultSet"]["headers"]
#print(pd.DataFrame(r["resultSet"]["rowSet"], columns = table_headers))
'''
temp_df1 = (pd.DataFrame(r["resultSet"]["rowSet"], columns = table_headers))
temp_df2 = pd.DataFrame({
    "Year": ["2012-13" for _ in range(len(temp_df1))],
    "Season_type": ["Regular%20Season" for _ in range(len(temp_df1))]
})

						
#print(temp_df2)		







temp_df3 = pd.concat([temp_df2, temp_df1], axis = 1)	
print(temp_df3)			
'''

df_cols = ["Year", "Season_type"] + table_headers

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "stats.nba.com",
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}


df = (pd.DataFrame(columns = df_cols))
season_types = ["Regular%20Season", "Playoffs"]
years = ["2012-13", "2013-14", "2014-15", "2015-16", "2016-17", "2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24"]
begin_loop = time.time()
for y in years:
    for s in season_types:
        api_url = "https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season="+y+"&SeasonType="+s+"&StatCategory=PTS"
        r = requests.get(url=api_url, headers=headers).json()  # Add parentheses to call json() method
        temp_df1 = pd.DataFrame(r["resultSet"]["rowSet"], columns=table_headers)
        temp_df2 = pd.DataFrame({
            "Year": [y for _ in range(len(temp_df1))],
            "Season_type": [s for _ in range(len(temp_df1))]})
        temp_df3 = pd.concat([temp_df2, temp_df1], axis=1)
        df = pd.concat([df, temp_df3], axis=0)
        print(f'Finished scraping data for the {y} {s}.')
        log = np.random.uniform(low=5, high=40)
        print(f"...waiting {round(log, 1)} seconds")
        time.sleep(log)

print(f"Process Completed Total run time:{round(time.time()-begin_loop)/60}")
df.to_excel("nba_player_data.xlsx", index=False)
print(df)
