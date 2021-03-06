### Import libraries
import pandas as pd
from datetime import datetime
import ast

PATH = 'credits_consumed.csv'


def generate_credit_summary(PATH):
    """
    Function that returns above dataframe 
    """
    ### Import Dataset
    df = pd.read_csv(PATH)

    ### Convert JSON into dataframe
    df = pd.DataFrame(df['RECORD_CONTENT'].apply(ast.literal_eval).values.tolist())

    ### change timestamp values into datetime format
    df['timestamp'] =pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    df['Date'] = df['timestamp'].dt.date

    df1 = df.groupby(['org_id', 'Date']).agg(
                region_id_cnt = ('region_id', pd.Series.nunique),
                resource_cnt = ('resource', pd.Series.nunique),
                user_id_cnt = ('user_id', pd.Series.nunique),
                credits_consumed_sum = ('credits_consumed', 'sum'),
                )

    df2 = df.groupby(['org_id', 'Date','resource'])['credits_consumed'].agg(total ='sum')
    df2 = df2.reset_index()

    df2 = pd.DataFrame(df2.groupby(['org_id', 'Date'])[['resource','total']].apply(lambda g: dict(g.values)),columns = ['resource_cnt'])

    df3 = df.groupby(['org_id', 'Date','region_id'])['credits_consumed'].agg(total ='sum')
    df3 = df3.reset_index()

    df3 = pd.DataFrame(df3.groupby(['org_id', 'Date'])[['region_id','total']].apply(lambda g: dict(g.values)),columns = ['region_cnt'])

    df_res = pd.merge(df1,df2,on =['org_id',	'Date'],how='left')
    df_res = pd.merge(df_res,df3,on =['org_id',	'Date'],how='left')
    
    return df_res


df_res = generate_credit_summary(PATH = PATH)
df_res.to_csv('summarized_data.csv')
