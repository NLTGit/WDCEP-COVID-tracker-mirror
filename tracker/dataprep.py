import pandas as pd
from tracker.config import CITIES, OPENTABLE_SEATEDYOY_PATH
from datetime import datetime

def get_compare_cities(dpath=CITIES):
    df = pd.read_csv(dpath)
    df.columns = ['city','is_contemporary']
    df['is_contemporary'] = df['is_contemporary']=='YES'
    return df

def ot_filter(df, dropcols=['Type']):
    # filter for all USA, all cities, and DC + washDC metro (and rename)
    usaidx = (df['Name'] == 'United States')
    dcidx = (df['Type'] == 'state') & (df['Name'] == 'District of Columbia')
    cityidx = (df['Type']=='city')
    df.loc[cityidx & (df['Name']=='Washington'), 'Name'] = 'Washington, DC (metro)'
    df = df.loc[usaidx | dcidx | cityidx, ~(df.columns.isin(dropcols))]
    return df.set_index('Name')

def get_opentable_all_cities(dpath=OPENTABLE_SEATEDYOY_PATH):
    df = pd.read_csv(dpath)
    return ot_filter(df)

def get_ot_comp_cities(cities, ot_global, verbose=False):
    idx = ot_global['Name'].isin(cities['city'])
    if verbose:
        print(f"these cities are not in the Open Table dataset:")
        print(cities.loc[~cities['city'].isin(ot_global['Name']), 'city'])
    return ot_global.loc[idx, :]

def get_ot_contemp_cities(cities, ot_global):
    idx = ot_global['Name'].isin(cities.loc[cities['is_contemporary'],'city'])
    return ot_global.loc[idx, :]



# def prep_ot():
#     cities = get_compare_cities()
#     ot_global = get_opentable_all_cities()
#     ot_comps = get_ot_comp_cities(cities, ot_global)
#     ot_contemps = get_ot_contemp_cities(cities, ot_global)
#     return ot_global, ot_comps, ot_contemps

def ot_ts_prep(data, window):
    data = data.T
    data.index = [datetime.strptime(f"2020/{i}", "%Y/%m/%d") for i in data.index]
    return data if window is None else data.rolling(window).mean()
