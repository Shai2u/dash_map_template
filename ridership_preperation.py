import pandas as pd

pd.options.display.max_columns = 999
if __name__ == "__main__":
    ridership = pd.read_csv('ridership.csv')
    ridership = ridership[ridership['Q'] == 2].copy().reset_index(drop=True)
    ridership['makat_dir'] = ridership['RouteID'].astype(
        str) + '-' + ridership['RouteDirection'].astype(str)
    ridership.to_csv('ridership_prepared.csv', index=False)
