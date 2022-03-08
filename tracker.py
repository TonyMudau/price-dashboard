import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from numpy.lib.twodim_base import triu_indices_from
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime, date
import requests
import datetime
#==========================================================================

"""
    In this project we create a price tracking dashboard using the Open price engine. 
    In the dashboard we make use of plotly and send requests to the ope API. 

"""
#==========================================================================


def request_data_ope(store, prodslist,date_range):
    response = requests.get(f'https://openpricengine.com/api/v0.1/{store}/products/query?list={prodlist}&range={date_range}')
    json_list = response.json()
    df = pd.DataFrame.from_records(json_list)
    emp = []
    for i in range(len(df)):
        price_date = df['Price over time'][i]
        details = df.iloc[:,:4].iloc[i]
        dates = pd.DataFrame.from_records(price_date).set_index('Date').T.reset_index(drop=True)
        tails = pd.DataFrame(details).T.reset_index(drop=True)
        v = pd.concat([tails,dates], axis=1)
        emp.append(v)
    final = pd.concat(emp)
    return final


# Load data
date_today = date.today().strftime("%Y-%m-%d")
latest_pnp_csv = pd.read_csv(r'C:\Users\mudau\Desktop\Food Prices API\Data\pnp\PnpMainTable.csv')
latest_pnpdrinks_csv = pd.read_csv(r'C:\Users\mudau\Desktop\Food Prices API\Data\pnpdrinks\PnpdrinksMainTable.csv')
latest_spar_csv = pd.read_csv(r'C:\Users\mudau\Desktop\Food Prices API\Data\spar\SparMainTable.csv')
latest_makro_csv = pd.read_csv(r'C:\Users\mudau\Desktop\Food Prices API\Data\makro\MakroMainTable.csv')
latest_makroliq_csv = pd.read_csv(r'C:\Users\mudau\Desktop\Food Prices API\Data\makrodrinks\MakrodrinksMainTable.csv')
latest_game_csv = pd.read_csv(r'C:\Users\mudau\Desktop\Food Prices API\Data\game\GameMainTable.csv')
latest_clicks_csv = pd.read_csv(r'C:\Users\mudau\Desktop\Food Prices API\Data\clicks\ClicksMainTable.csv')
latest_dischem_csv = pd.read_csv(r'C:\Users\mudau\Desktop\Food Prices API\Data\dischem\DischemMainTable.csv')

def get_prodnames():
    shop =  pd.read_csv(r'C:\Users\mudau\Desktop\Food Prices API\Data\pnp\PnpMainTable.csv')
    prod_names = shop['Product Name']
    prods_list_json =[]
    for i in range(len(prod_names)):
        names = {"label": shop['Product Name'][i], 'value': shop['Product Name'][i]}
        prods_list_json.append(names)
    return prods_list_json





# Instanciate the app
app = dash.Dash(__name__, meta_tags = [{"name": "viewport", "content": "width=device-width"}])

# Build layout
app.layout = html.Div(
	[
		# (First Row): Title
		html.Div(
			[
				# (Column 1): Title
				html.Div(
					[
						html.Div(
							[
								# Title
								html.H1(
									children = "Daily Price Tracker",
									style = {
										"margin-bottom": "0px",
										"color": "white"
									}
								),
								# Subtitle
								html.H5(
									children = f"{date_today}",
									style = {
										"margin-top": "0px",
										"color": "white"
									}
								)
							]
						)
					],
					className = "six column",
					id = "title"
				)
			],
			id = "header",
			className = "row flex-display",
			style = {
				"margin-bottom": "25px"
			}
		),
		
		# (Third Row): Plots
		html.Div(
			[
				# (Column one) User inputs
			html.Div(
					[
						# Title for first dropdown
						html.P(
              children = "Select Country",
              className = "fix_label",
              style = {
                "color": "white"
              }
            ),
            # country dropdown
            dcc.Dropdown(
							id = "countries",
							multi = False,
							searchable = True,
							value = "South Africa",
							placeholder = "South Africa",
							options = [{'label': 'South Africa', 'value': 'South Africa'}],
							className = "dcc_compon"
						),
                        
             html.P(
              children = "Select Store",
              className = "fix_label",
              style = {
                "color": "white"
              }
            ),
            # store dropdown
            dcc.Dropdown(
							id = "shop",
							multi = False,
							searchable = True,
							value = "Pick n Pay",
							placeholder = "Select Store",
							options = [{'label': 'Pick n Pay', 'value': 'pnp'},
                                       {'label': 'Pick n Pay Liquor', 'value': 'pnpliq'},
                                       {'label': 'Spar', 'value': 'Spar'},
                                       {'label': 'Makro', 'value': 'Makro'},
                                       {'label': 'Mako Liquor', 'value': 'makroliq'},
                                       {'label': 'Game', 'value': 'Game'},
                                       {'label': 'Dischem', 'value': 'Dischem'},
                                       {'label': 'Clicks', 'value': 'Clicks'},],
							className = "dcc_compon"
						),        
                        
                        
                        
            # Title for second dropdown
            html.P(
              children = "Add products",
              className = "fix_label",
              style = {
                "color": "white"
              }
            ),
            # products dropdown
            dcc.Dropdown(id = "productnames", 
                         multi=True),
                        
                        
            
            # Title for range slider
            html.P(
              children = "Select Date Range",
              className = "fix_label",
              style = {
                "color": "white"
              }
            ),

            # Range slider
            dcc.RangeSlider(
							id = "dates_range",
              #min = datetime.date(2021, 12, 15),
              #max = datetime.date(2022, 3, 7),
              dots = False,
              #value = [min, max]
						)
          ],
          className = "create_container three columns"
        ),
        
 #=========================Charts=========================-====================       
        
        # (Column two) Bars and line chart
        html.Div(
          [
            dcc.Graph(
              id = "bar_chart",
              config = {
                "displayModeBar": "hover"
              }
            )
          ],
          className = "create_container six columns"
        ),
        
        
        
        
        
        
        
        
        # (Column three) Pie chart
        html.Div(
          [
            dcc.Graph(
              id = "pie_chart",
              config = {
                "displayModeBar": "hover"
              }
            )
          ],
          className = "create_container three columns"
        )
      ],
      className = "row flex-display"
    )
  ],
  id = "mainContainer",
	style = {
		"display": "flex",
		"flex-direction": "column"
	}
)

#=============================Call backs =========================================#
# Update second dropdown
@app.callback(
  Output(
    component_id = "productnames",
    component_property = "options"
  ),
  Input(
    component_id = "shop",
    component_property = "value"
  )
)


# This function sends a request to the OPE which returns product names of a store for users to select
def get_prodnames(shop):
    response = requests.get(f'https://openpricengine.com/api/v0.1/{shop}/products')
    json_list = response.json()
    prod = json_list.values()
    prod_names = list(prod)
    prods_list_json =[]
    for i in (prod_names):
        names = {"label": i, 'value': i}
        prods_list_json.append(names)
    return prods_list_json



#---------------------------------------------
# Update line and bars char
@app.callback(
  Output(
    component_id = "bar_chart",
    component_property = "figure"
  ),
  Input(
    component_id = "shop",
    component_property = "value"
  ),
  Input(
    component_id = "productnames",
    component_property = "value"
  ),
  Input(
    component_id = "dates_range",
    component_property = "value"
  )
)


def create_plot(shop, productnames, dates_range):
    response = requests.get(f'https://openpricengine.com/api/v0.1/{shop}/products/query?list={productnames}&range=2022-03-01to2022-03-07')
    json_list1 = response.json()
    df = pd.DataFrame.from_records(json_list1)
    emp = []
    for i in range(len(df)):
        price_date = df['Price over time'][i]
        details = df.iloc[:,:4].iloc[i]
        dates = pd.DataFrame.from_records(price_date).set_index('Date').T.reset_index(drop=True)
        tails = pd.DataFrame(details).T.reset_index(drop=True)
        all_table = pd.concat([tails,dates], axis=1)
        emp.append(all_table)
    data_table = pd.concat(emp)
    DF = data_table.iloc[:,3:].T
    DF.columns = DF.iloc[0]
    DF.drop(DF.index[0], inplace = True)  
    k = productnames
    print(k)
    final = DF[k]
    fig = px.line(final, labels=dict(value = 'Price (ZAR)', index= 'Date'),markers=False, title=f"{shop}")
    return fig


# Run the app
if __name__ == "__main__":
  app.run_server(debug = True, port=8080)
