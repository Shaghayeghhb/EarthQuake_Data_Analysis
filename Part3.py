import pandas as pd
import numpy as np


def initialize_usgs():
    usgs_df = pd.read_csv('JAPAN_USGS.csv')

    print('USGS Shape:', usgs_df.shape)

    usgs_df['time'] = pd.to_datetime(usgs_df['time'], errors='coerce')
    usgs_df['updated'] = pd.to_datetime(usgs_df['updated'], errors='coerce')
    numeric_cols = ['nst', 'gap', 'magNst', 'mag', 'depth', 'dmin', 'rms',
                    'horizontalError', 'depthError', 'magError']
    for col in numeric_cols:
        if col in usgs_df.columns:
            usgs_df[col] = pd.to_numeric(usgs_df[col], errors='coerce').astype(float)

    usgs_df_del = usgs_df.dropna()

    usgs_df_del['Month'] = usgs_df_del['time'].dt.month

    usgs_df_del['Category'] = ''
    for index in usgs_df_del.index:
        mag = usgs_df_del.loc[index, 'mag']
        if mag < 5:
            usgs_df_del.loc[index, 'Category'] = 'Weak'
        elif 5 <= mag <= 6:
            usgs_df_del.loc[index, 'Category'] = 'Medium'
        else:
            usgs_df_del.loc[index, 'Category'] = 'Strong'
    return usgs_df_del

def initialize_geofon() :
    geofon_df = pd.read_csv('JAPAN_GEOFON.csv')

    print('GEFON Shape:', geofon_df.shape)

    geofon_df['time'] = pd.to_datetime(geofon_df['time'], errors='coerce')
    geofon_df['depth'] = pd.to_numeric(geofon_df['depth'], errors='coerce').astype(float)

    geofon_df_del = geofon_df.dropna()

    geofon_df_del['Month'] = geofon_df_del['time'].dt.month

    geofon_df_del['Category'] = ''
    for index in geofon_df_del.index:
        mag = geofon_df_del.loc[index, 'mag']
        if mag < 5:
            geofon_df_del.loc[index, 'Category'] = 'Weak'
        elif 5 <= mag <= 6:
            geofon_df_del.loc[index, 'Category'] = 'Medium'
        else:
            geofon_df_del.loc[index, 'Category'] = 'Strong'
    return geofon_df_del

def mag_count_and_mean (df):
    usgs_group_c_m = df.groupby(['Month', 'Category'])['mag'].agg(['count', 'mean']).reset_index()
    usgs_group_c_m.rename(columns={'count': 'Count', 'mean': 'Mean'}, inplace=True)
    return usgs_group_c_m

def area(df):
    def area_name(place):
        place = place.strip()
        if ' of ' in place:
            return place.split(' of ')[-1].split(',')[0].strip()
        elif ',' in place:
            return place.split(',')[0].strip()
        else:
            return place

    df['Area Name'] = df['place'].apply(area_name)
    return df

def area_mag_count(df):
    temp= area(df)
    eq_count = temp.groupby('Area Name')['mag'].count().sort_values(ascending=False)
    eq_count_df = eq_count.reset_index()  # To_DataFrame
    eq_count_df.columns = ['Area Name', 'Earthquake Count']
    return eq_count_df

def area_mean_mag_and_depth(df):
    temp= area(df)
    mean_mag_and_depth = temp.groupby('Area Name')[['mag', 'depth']].mean().sort_values(by=['mag', 'depth'],
                                                                                                ascending=[False,
                                                                                                           False])
    return mean_mag_and_depth
def area_max_mag_and_depth(df):
    temp  = area(df)
    max_mag_and_depth = temp.groupby('Area Name')[['mag', 'depth']].max()
    max_mag_and_depth_sorted = max_mag_and_depth.sort_values(by=['mag', 'depth'], ascending=[False, False])
    return max_mag_and_depth_sorted

def geofon_array(df):
    geofon_array_mag = np.array(df['mag'])
    geofon_array_place = np.array(df['place'])
    geofon_array_time = np.array(df['time'])
    geofon_array_depth = np.array(df['depth'])
    return geofon_array_mag, geofon_array_place, geofon_array_time, geofon_array_depth

def usgs_array(df):
    usgs_array_time = np.array(df['time'])
    usgs_array_latitude = np.array(df['latitude'])
    usgs_array_longitude = np.array(df['longitude'])
    usgs_array_depth = np.array(df['depth'])
    usgs_array_mag = np.array(df['mag'])
    usgs_array_place = np.array(df['place'])
    return usgs_array_time, usgs_array_latitude, usgs_array_longitude, usgs_array_depth, usgs_array_mag, usgs_array_place

def usgs_distance (df) :
    temp = usgs_array(df)
    pal = temp[5]
    lat = temp[1]
    lon = temp[2]
    for i in range(len(temp[5])-1 , 0 ,- 1):
        x1 = lat[i]
        x2 = lat[i - 1]
        y1 = lon[i]
        y2 = lon[i - 1]
        dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        print(f'the distant between {pal[i]} and {pal[i - 1]} earthquake is {dist}')

def geofon_disitance ():
    print("longitude and latitude are required to calculate geofon disitance ")
    print("geofon does not give it")
    return

def Statistical_calculations (array) :

    pass
