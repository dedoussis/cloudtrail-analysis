
# coding: utf-8

# In[123]:


import json
import matplotlib
import pandas as pd
from pandas import DataFrame as df


# In[210]:


with open('event_history.json') as f:
    data = json.load(f)
    
records = df(data['Records'])


# In[211]:


records.index = pd.to_datetime(records['eventTime'])
print(f"{records.shape[0]} CloudTrail events traced from {records.index.min()} to {records.index.max()}")
records.head()
records = pd.concat([records.drop(['userIdentity'], axis=1), records['userIdentity'].apply(pd.Series)], axis=1)


# In[212]:


def daily_count_plot(daily_count):
    fig = daily_count.plot(x='Time', y='Count', title='CloudTrail events over time')
    fig.set(xlabel='Date', ylabel='Count');


# In[213]:


print('Plotting overall activity...')
daily_count = records['eventTime'].resample('D').count()
daily_count_plot(daily_count)


# In[214]:


USERNAME = 'dimitrios.dedoussis'

print(f'Plotting {USERNAME} activity...')
user_records = records[records['principalId'].str.contains(USERNAME, na=False)]
user_daily_count = user_records['eventTime'].resample('D').count()
daily_count_plot(user_daily_count)


# In[215]:


print(f'Plotting correlation between {USERNAME} and overall activity...')

normalise = lambda data_df: (data_df - data_df.mean()) / (data_df.max() - data_df.min()) 
daily_count_plot(normalise(daily_count))
daily_count_plot(normalise(user_daily_count))


# In[223]:


start_date = user_daily_count.idxmax()
print(f'{USERNAME} maximum daily activity was detected on {start_date}')

end_date = start_date + pd.DateOffset(days=1)
mask = (user_records.index > start_date) & (user_records.index <= end_date)
user_max_daily = user_records.loc[mask]
print(f'Events of {USERNAME} on {start_date}:')
print(f'TOTAL of {user_max_daily.shape[0]} events:')
user_max_daily['eventSource'].value_counts()

