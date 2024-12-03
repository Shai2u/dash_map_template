import pandas as pd
import geopandas as gpd
pd.options.display.max_columns = 999

if __name__ == "__main__":
    routes = gpd.read_file('routes_israel_4326.geojson')
    ridership = pd.read_csv('ridership_prepared.csv')
    routes['makat_dir'] = routes['route_desc'].apply(
        lambda p: p.split('-')[0] + '-' + p.split('-')[1])
    routes = routes.merge(ridership, how='left', on='makat_dir')
    routes['AgencyName'].unique()

    ['מטרופולין', 'תנופה', 'קווים',
     'דן בדרום', 'אקסטרה', 'נתיב אקספרס', 'אגד',
     'דן', 'סופרבוס', 'דן באר שבע',
     'אקסטרה ירושלים',  'בית שמש אקספרס', 'גלים']

    routes = routes[routes['AgencyName'].isin(['מטרופולין', 'תנופה', 'קווים',
                                               'דן בדרום', 'אקסטרה', 'נתיב אקספרס', 'אגד',
                                               'דן', 'סופרבוס', 'דן באר שבע',
                                               'אקסטרה ירושלים',  'בית שמש אקספרס', 'גלים'])].copy().reset_index(drop=True)
    routes['geometry'] = routes.simplify(0.0001)
    routes.to_file('routes_with_ridership.geojson')
