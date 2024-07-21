import dash
from dash import dcc, html, ctx
import datetime
import horse_history
import pandas as pd
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

class Horse:
  def __init__(self, color, age, dr, weight, dam, jockey, finish_time=0):
      self.color = color
      self.age = age
      self.dr = dr
      self.weight = weight
      self.dam = dam
      self.jockey = jockey
      self.finish_time = finish_time

# Calculate Horse Finish Time
def getHorseFinishTime(horse: Horse, distance, race_class, month, location, ml_model):
    distance_km = int(distance) / 1000
    data = pd.DataFrame({
        'horse_color': [horse.color],
        'horse_age': [horse.age],
        'race_class': [race_class],
        'weight': [horse.weight],
        'dr': [horse.dr],
        'jockey': [horse.jockey],
        'distance_km': [distance_km],
        'distance': [distance],
        'quarter': [horse_history.getQuarter(month)], 
        'horse_dam': [horse.dam],
        'location': [location],
    })

    fieldsToEncodeWithMedian = ['jockey', 'horse_color', 'horse_dam']
    for f in fieldsToEncodeWithMedian:
      data[f] = horse_history.encodeWithMedianRank(data[f], f)

    horse_history.applyNoOfTurns(data)
    predict_data = data.drop(columns=['location', 'distance'], axis=1)

    fillInNAByMeanField = ['jockey', 'horse_dam']
    for f in fillInNAByMeanField:
        horse_history.fillinMissingValueByMean(predict_data, f)
    
    print(predict_data)

    speed = ml_model.predict(predict_data)
    time = distance / speed[0]
    return time  

# Convert finish time to display format
def getDisplayFinishTime(finish_time):
    minutes = int(finish_time // 60)
    seconds = finish_time % 60
    return f"{minutes}:{seconds:05.2f}"

# Convert encoded value to user input options
def getFeatureOptions(feature_name):
  if feature_name == "race_class":
    return ['1', '2', '3', '3R', '4', '4R', '4YO', '5', 'G1', 'G2', 'G3', 'GRIFFIN']
  elif feature_name == "distance":
    return [1000, 1200, 1400, 1600, 1650, 1800, 2000, 2200, 2400]
  elif feature_name == "location":
    return ["ST", "HV"]
  elif feature_name == "horse_color":
    return ["Bay", "Black", "Brown", "Chestnut", "Dark Bay", "Grey"]
  elif feature_name == "horse_age":
    return list(range(1, 11))
  elif feature_name == "dr":
    return list(range(1, 15))

def run(model):
    race_class_options = getFeatureOptions("race_class")
    distance_options = getFeatureOptions("distance")
    location_options = getFeatureOptions("location")
    horse_color_options = getFeatureOptions("horse_color")
    horse_age_options = getFeatureOptions("horse_age")
    dr_options = getFeatureOptions("dr")

    # Link boostrap css
    external_stylesheets = [
       'https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/litera/bootstrap.min.css'
    ]

    # Create the Dash app
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    colors = {
        "background": "#fff",
    }

    # Define the layout
    app.layout = html.Div(
        style={"backgroundColor": colors["background"]},
        children=[
            html.H1(
                children="HKJC Prediction", style={"textAlign": "center"},
            ),

            html.Div(style={"display": "flex", "flexDirection":"row"},
                children=[
                    html.Div(
                        style={"padding": 10, "flex": 2, "padding": "20px", "backgroundColor": "rgb(238, 238, 238)"},
                        children=[
                            html.H2(
                                children="Race", style={"textAlign": "center"},
                            ),
                            html.Div(children=[
                                html.Div([
                                    html.Div(children=[
                                        html.Label("Race Class"),
                                        dcc.Dropdown(
                                            id="race_class_dropdown",
                                            options=race_class_options,
                                            value=race_class_options[0],
                                            clearable=False
                                        ),

                                        html.Br(),
                                        html.Label("Month"),
                                        html.Br(),
                                        dcc.Input(
                                            id="month_input",
                                            placeholder="Input race month",
                                            type="number",
                                            value=datetime.datetime.now().month,
                                            min=1,
                                            max=12,
                                            step=1,
                                            className="form-control"
                                        ),
                                    ]),
                                ], style={"padding": 10, "flex": 1}),

                                html.Div([
                                    html.Div(children=[
                                        html.Label("Distance"),
                                        html.Br(),
                                        dcc.Dropdown(
                                            id="distance_dropdown",
                                            options=distance_options,
                                            value=distance_options[0],
                                            clearable=False
                                        )
                                    ]),
                                ], style={"padding": 10, "flex": 1}),

                                html.Div([
                                    html.Div(children=[
                                        html.Label("Location"),
                                        dcc.Dropdown(
                                            id="location_dropdown",
                                            options=location_options,
                                            value=location_options[0],
                                            clearable=False
                                        ),
                                    ])
                                ], style={"padding": 10, "flex": 1}),
                            ], style={"display": "flex", "flexDirection":"row"}),

                            html.Br(),
                            html.H2(
                                children="Horse", style={"textAlign": "center"},
                            ),
                            html.Div(children=[
                                html.Div(children=[
                                    html.Label("Color"),
                                    dcc.Dropdown(
                                        id="horse_color_dropdown",
                                        options=horse_color_options,
                                        value=horse_color_options[0],
                                        clearable=False
                                    ),

                                    html.Br(),
                                    html.Label("Weight in pounds (900lb.-1600lb.)"),
                                    html.Br(),
                                    dcc.Input(
                                        id="horse_weight_input",
                                        placeholder="Input horse weight",
                                        type="number",
                                        value=1000,
                                        min=900,
                                        max=1600,
                                        step=1,
                                        className="form-control"
                                    ),
                                ], style={"padding": 10, "flex": 1}),

                                html.Div(children=[
                                    html.Label("Age"),
                                    dcc.Dropdown(
                                        id="horse_age_dropdown",
                                        options=horse_age_options,
                                        value=horse_age_options[0],
                                        clearable=False
                                    ),
                                    
                                    html.Br(),
                                    html.Label("Horse Dam"),
                                    html.Br(),
                                    dcc.Input(
                                        id="horse_dam_input",
                                        placeholder="Input horse dam in English",
                                        type="text",
                                        className="form-control"
                                    ),
                                ], style={"padding": 10, "flex": 1}),

                                html.Div(children=[
                                    html.Label("Draw"),
                                    dcc.Dropdown(
                                        id="horse_dr_dropdown",
                                        options=dr_options,
                                        value=dr_options[0],
                                        clearable=False
                                    ),

                                    html.Br(),
                                    html.Label("Jockey"),
                                    html.Br(),
                                    dcc.Input(
                                        id="jockey_input",
                                        placeholder="Input jockey in English",
                                        type="text",
                                        className="form-control"
                                    ),
                                ], style={"padding": 10, "flex": 1}),
                            ], style={"display": "flex", "flexDirection":"row"}),

                            html.Div(children=[
                                html.Button("Add Horse",
                                    id="add_horse_button",
                                    className="btn btn-primary",
                                    style={"marginRight": "20px"}),
                                html.Button("Clear",
                                    id="clear_button",
                                    className="btn btn-outline-primary")
                            ], style={"textAlign": "center"}),
                        ]
                    ),
                    html.Div(
                        style={"padding": 10, "flex": 1},
                        children=[
                            html.H2(
                                children="Result", style={"textAlign": "center"}
                            ),
                            html.Div(children="No horse", id="output_label", style={ "textAlign": "center", "white-space":"pre-wrap"})
                    ]),
                ]
            ),
        ]
    )

    output_horse_list = []

    # Define the callback function for updating the graph
    @app.callback(
        Output('output_label', 'children'),
        Output('race_class_dropdown', 'disabled'),
        Output('distance_dropdown', 'disabled'),
        Output('location_dropdown', 'disabled'),
        Output('month_input', 'disabled'),
        [Input('race_class_dropdown', 'value'),
        Input('distance_dropdown', 'value'),
        Input('location_dropdown', 'value'),
        Input('month_input', 'value'),
        Input('horse_color_dropdown', 'value'),
        Input('horse_age_dropdown', 'value'),
        Input('horse_weight_input', 'value'),
        Input('horse_dr_dropdown', 'value'),
        Input('jockey_input', 'value'),
        Input('horse_dam_input', 'value'),
        Input('add_horse_button', 'n_clicks'),
        Input('clear_button', 'n_clicks'),
        ],
    )
    def update_output(selected_race_class, selected_distance, selected_location, selected_month, selected_color, selected_age, selected_weight, selected_dr, selected_jockey, selected_dam, add_clicks, clear_clicks):
        if "add_horse_button" == ctx.triggered_id:
            # Display race content
            msg = f"Race Class: {selected_race_class}\nDistance: {selected_distance}\nLocation: {selected_location}\nMonth: {selected_month}\n\n"
            
            # Display horse finish time
            horse = Horse(selected_color, selected_age, selected_dr, selected_weight, selected_dam, selected_jockey)
            predict_finishtime = getHorseFinishTime(horse, selected_distance, selected_race_class, selected_month, selected_location, model)
            horse.finish_time = predict_finishtime
            output_horse_list.append(horse)
            for index, output_horse in enumerate(output_horse_list):
                msg += f"Horse {index+1}, Draw:{output_horse.dr}, Finish Time: {getDisplayFinishTime(output_horse.finish_time)}\n"

            # Display winner
            winner_index, winner = min(enumerate(output_horse_list), key=lambda x: x[1].finish_time)
            msg += f"\n🏆 Winner: Horse {winner_index+1} with finish time: {getDisplayFinishTime(winner.finish_time)} "
            return html.Div(msg), True, True, True, True
        elif "clear_button" == ctx.triggered_id:
            output_horse_list.clear()
            return html.Div("Clear horse"), False, False, False, False
        else:
            raise PreventUpdate

    # Run the app
    app.run_server(debug=True)
