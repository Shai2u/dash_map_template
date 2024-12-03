from dash import Dash, dcc, html, Input, Output
import dash_leaflet as dl
import dash_leaflet.express as dlx
import json


import geopandas as gpd
import pandas as pd
pd.options.display.max_columns = 150
# Load the data
ridership = gpd.read_file(
    'routes_with_ridership.geojson')

# Agencies
agencies = ridership['AgencyName'].unique()
agencies_options = [{'label': agency, 'value': agency} for agency in agencies]
# Clusters
clusters = ridership['ClusterName'].unique()
cluster_options = [{'label': cluster, 'value': cluster}
                   for cluster in clusters]
# Routes
route_names = ridership['route_short_name'].unique()
route_names_options = [{'label': route_name, 'value': route_name}
                       for route_name in route_names]

geojson = {
    "type": "FeatureCollection",
    "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[35.1, 31.5], [35.2, 31.6], [35.3, 31.7]]
                },
                "properties": {"name": "Polyline"}
            }
    ]
}
geojson2 = ridership.iloc[0:1].__geo_interface__
print(ridership.head())

app = Dash()
app.layout = html.Div([
    html.Div(
        [
            html.Div(dl.Map([dl.TileLayer(),
                             dl.GeoJSON(id='lines_geojson', data=geojson2,
                                        options=dict(style=dict(color='blue')), zoomToBounds=True)
                             ],
                            center=[32.5, 34],
                            zoom=8,
                            style={'height': '90vh'},
                            id='main_map'
                            ))],
        style={'width': '68%', 'display': 'inline-block', 'margin-right': '2%'},
    ),
    html.Div([html.Div("print hello world"),
              html.Div([
                  html.Label('Agency'),
                  dcc.Dropdown(
                      id='agencies-dropdown',
                      options=agencies_options,
                      value=agencies_options[0]['value']
                  ),
                  html.Label('Clusters'),
                  dcc.Dropdown(
                      id='clusters-dropdown',
                      options=cluster_options,
                      value=cluster_options[0]['value'],
                      disabled=True
                  ),
                  html.Label('Routes'),
                  dcc.Dropdown(
                      id='routes-dropdown',
                      options=route_names_options,
                      value=route_names_options[0]['value'],
                      disabled=True
                  )
              ]),
              html.Div(
                  dl.Map([dl.TileLayer(url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png'), dl.Polygon(positions=[], id='main_map_footprint_polygon', color='red', fillOpacity=0)],
                         center=[32, 34],
                         zoom=7,
                         style={'height': '50vh'},
                         id='env_map',
                         dragging=False,
                         zoomControl=False,
                         scrollWheelZoom=False,
                         doubleClickZoom=False,
                         boxZoom=False,
                         )
    )
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Div(id='temp')

])


@app.callback(
    [Output('clusters-dropdown', 'options'),
     Output('clusters-dropdown', 'disabled')],
    [Input('agencies-dropdown', 'value')]
)
def update_clusters_dropdown(selected_agency):
    filtered_clusters = ridership[ridership['AgencyName']
                                  == selected_agency]['ClusterName'].unique()
    return [[{'label': cluster, 'value': cluster} for cluster in filtered_clusters], False]


@app.callback(
    [Output('routes-dropdown', 'options'),
     Output('routes-dropdown', 'disabled')],
    [Input('clusters-dropdown', 'value'), Input('agencies-dropdown', 'value')]
)
def update_routes_dropdown(cluster, agency):
    filtered_routes = ridership[(ridership['AgencyName'] == agency) & (
        ridership['ClusterName'] == cluster)]['route_short_name'].unique()

    return [[{'label': route, 'value': route} for route in filtered_routes], False]


@app.callback(
    [Output('lines_geojson', 'data')],
    [Input('agencies-dropdown', 'value'), Input('clusters-dropdown',
                                                'value'), Input('routes-dropdown', 'value')]
)
def update_map_route_layer(agency, cluster, route):

    export_geojson = geojson2
    ridership_filtered = ridership.loc[(ridership['AgencyName'] == agency) & (
        ridership['ClusterName'] == cluster) & (ridership['route_short_name'] == route)].copy()
    subset = ridership_filtered[['fid', 'geometry']].iloc[0:1].copy()
    subset['fid'] = subset['fid'].astype(int)
    export_geojson = subset.__geo_interface__
    return [export_geojson]


@app.callback(
    Output('main_map_footprint_polygon', 'positions'),
    [Input('main_map', 'bounds')]
)
def update_env_map_center(bounds):
    if bounds is None:
        return []
    return [[bounds[0][0], bounds[0][1]], [bounds[1][0], bounds[0][1]], [bounds[1][0], bounds[1][1]], [bounds[0][0], bounds[1][1]]]


if __name__ == '__main__':
    app.run_server()
