import dash
from dash.dependencies import Input, Output, State
from numpy.lib.twodim_base import triu_indices_from
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime, date
import requests
import datetime
import dash_bootstrap_components as dbc
from dash import Output, State, html, no_update, dcc
import random
import webbrowser
import ast
# Import the email modules we'll need
import smtplib
from email.message import EmailMessage
#==========================================================================

"""
    In this project we create a price tracking dashboard using the Open price engine. 
    In the dashboard we make use of plotly and send requests to the ope API. 

"""
#==========================================================================


###=========GLOBAL FUNCTIONS=======================########


date_today = date.today().strftime("%Y-%m-%d")



#VAPOR, QUARTZ
# Instanciate the app
app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.VAPOR], meta_tags = [{"name": "viewport", 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,' }])

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
									children = "Daily Price Tracker 🍜",
									style = {
										"margin-bottom": "0px",
										"color": "white",
                                        "font-weight": "bold"
                                        
									}
								),
								# Subtitle
								html.H5(
									children = f"{date_today}",
									style = {
										"margin-top": "0px",
										"color": "white",
                                        
									}
								),
                        html.Div(
                            [
                            dbc.ButtonGroup(
                                [dbc.Button("About", id="open-offcanvas", n_clicks=0),
                                 dbc.Offcanvas(
                                            [html.P(
                                                "Daily Price tracker is a free to use dashboard that allows consumers to see the historical "
                                                "prices of their favourite products from retail stores. This is to help consumers compare prices and find the best time "
                                                "to buy a product at the best price. "
                                                "The Daily Price tracker  uses the Openpricengine API to get realtime price data."
                                                "You are able to set email notifications for price changes on products. "),
                                            dbc.Button("Buy developer a pizza 😉",id="simple-toast-toggle1",n_clicks=0),
                                                dbc.Toast(
                                                    [html.P("FNB"),html.P("Acc 62530854589")],
                                                    id="simple-toast1",
                                                    header="Donate",
                                                    icon="success",
                                                    dismissable=True,
                                                    is_open=False,
                                                    #syle="Secondary"
                                                ),],
                                            id="offcanvas",
                                            title="About Daily Price Tracker",
                                            is_open=False),
            
                                #---Track button
                             dbc.Button("Track", id="open-offcanvas1", n_clicks=0),
                                 dbc.Offcanvas(
                                            [html.Span(id="thanks", style={"verticalAlign": "middle"}),
                                            html.P("If you would like price change notifications on the following selected "
                                                     "products, click 'Notify Me'"),
                                             html.P(id="prods"),
                                             html.P(' '),
                                             dbc.Row([
                                                                dbc.Label("Email address"),
                                                                dbc.Input(type="email", id="emailinput"),
                                                                html.P(' '),
                                                                dbc.Button("Notify Me", id="notify",n_clicks=0, color="primary"),
                                                                
                                                                ]),
                                             
                                                ],
                                            id="offcanvas1",
                                            title="Track",
                                            is_open=False,
                                            placement="end"),],
                                size="lg",
                                style = {"color":"danger"},
                                className="gap-2 col-6 mx-auto",
                            ),
                              ],   
                                     ),                    
							]
						)
					],
					className = "nine column",
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
							value = "pnp",
							placeholder = "Select Store",
							options = [{'label': 'Pick n Pay', 'value': 'pnp'},
                                       {'label': 'Pick n Pay Liquor', 'value': 'pnpliq'},
                                       {'label': 'Spar', 'value': 'Spar'},
                                       {'label': 'Makro', 'value': 'Makro'},
                                       {'label': 'Mako Liquor', 'value': 'makroliq'},
                                       {'label': 'Game', 'value': 'Game'},
                                       {'label': 'Dischem', 'value': 'Dischem'},
                                       {'label': 'Clicks', 'value': 'Clicks'},],
							className = "fix_label"
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
                           value = ['Jacobs Kronung Instant Coffee 200g', 'PnP Potatoes 7kg'],
                         multi=True,
                         style = {
								"color": "white"}
                         ),                    
            
            # Title for Date range
            html.P(
              children = "Select Date Range",
              className = "fix_label",
              style = {
                "color": "white"
              }
            ),

            #Date range 
            dcc.DatePickerRange(
                    id='dates_range',
                    min_date_allowed=date(2021, 11, 15),
                    max_date_allowed=date(2022, 9, 19),
                    initial_visible_month=date(2022, 2, 24),
                    start_date= date(2022, 2, 24),
                    end_date=date_today,
                    #end_date = date(2022, 3, 16),
                    style = {
                        "color": "green",
                        "background-color": "#010915",
                        "display": "flex",
                      },
             className = "dcc_compon"
        ), 
        html.Span(id="prod", style={"verticalAlign": "middle"}),],
          className = "create_container three columns"
        ),
        
        
 #=========================Charts=========================-====================       
        
        # (Column two) Bars and line chart
        html.Div(
          [
            dcc.Graph(
              id = "bar_chart",
              config = {
                "displayModeBar": False
              }
            )
          ],
          className = "create_container eight columns g-0 ms-auto flex-nowrap mt-3 mt-md-0"
        )
        
        
       #===== (Column three) Pie chart

      ],
      className = "row flex-display .col-sm-"
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
    response = requests.get(f'https://openpricengine.com/api/v0.1/{shop}/products', timeout=150)
    json_list = response.json()
    prod = json_list.values()
    prod_names = list(prod)
    prods_list_json =[]
    for i in (prod_names):
        names = {"label": i, 'value': i}
        prods_list_json.append(names)
    print("got names")
    return prods_list_json



#---------------------------------------------
# Update line and bars char
@app.callback(
  Output(
    component_id = "bar_chart",
    component_property = "figure"
  ),
    Output(
    component_id = "prods",
    component_property = "children"
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
    component_property = "start_date"
  ),
  Input(
    component_id = "dates_range",
    component_property = "end_date"
  ),
)

# This function creates the figure
def create_plot(shop, productnames, start_date, end_date):
    response = requests.get(f'https://openpricengine.com/api/v0.1/{shop}/products/query?list={productnames}&range={start_date}to{end_date}')
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
    data_tables = pd.concat(emp)
    data_table = data_tables.drop(labels=['Store','Category','Product URL'], axis=1)
    DF = data_table.T
    DF.columns = DF.iloc[0]
    DF.drop(DF.index[0], inplace = True) 
    selectedprods = productnames
    final = DF[selectedprods]
    print(final)
    fig = px.line(final, labels=dict(value = 'Price (ZAR)', index= 'Date'), title=f"{shop}")
    fig.update_layout(annotations=[], overwrite=True)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1))
    selected = []
    for i in selectedprods:
        selected.append(i + ', ')
    print(selected)
    return fig, [i for i in selected]


#-------------------------------------------------------------------------------------

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open
    
#------------------------------------------------------------------------------------

@app.callback(
    Output("offcanvas1", "is_open"),
    Input("open-offcanvas1", "n_clicks"),
    [State("offcanvas1", "is_open")],
)
def toggle_offcanvas1(n1, is_open):
    if n1:
        return not is_open
    return is_open
     
#------------------------------------------------------------------------------------
   
@app.callback(
    Output("simple-toast1", "is_open"),
    [Input("simple-toast-toggle1", "n_clicks")],
)
def open_toast(n):
    if n == 0:
        return no_update
    return True

#--------------------------------------------------------------------------------


@app.callback(
  Output(
    component_id = "thanks",
    component_property = "children"
  ),
  Input(
    component_id = "productnames",
    component_property = "value"
  ),
    Input(
    component_id = "emailinput",
    component_property = "value"
  ),
  Input(
    component_id = "notify",
    component_property = "n_clicks"
  )
)


#This function sends user an email
def send_user_a_email(emailinput, productnames, notify):
    if notify == 0:
        return no_update
    msg = EmailMessage()
    message = """We will notify you when the following product prices change 😎. %s
    Visit: https://www.openpricengine.com/. To gain access to the same API we use! 
    
    Maybe developer does deserve a pizza 😉?

    """ % (emailinput)
    msg.set_content(message)
    print(emailinput, productnames, notify)
    msg['Subject'] = 'Price Tracker Notification.'
    msg['From'] = 'pricedata@learningtool.co.za'
    msg['To'] = [f'{productnames}']
    # Send the message via our own SMTP server.
    s = smtplib.SMTP('mail.learningtool.co.za', 25)
    print('about to login')
    s.login('pricedata@learningtool.co.za', 'BEo3kno')
    with open('ope.jpeg', 'rb') as f:
        img_data = f.read()
    msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename='ope.jpeg')
    s.send_message(msg)
    print('sent')
    s.quit()
    return "Awesome! You will be notified 🥂"









# Run the app
if __name__ == "__main__":
  app.run_server(debug =True, port=8080)
