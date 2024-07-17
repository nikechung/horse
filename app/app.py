import dash
from dash import dcc, html, ctx
import datetime
import horse_history
import pandas as pd

class Horse:
  def __init__(self, color, age, draw, weight, sire, dam, jockey, score):
      self.color = color
      self.age = age
      self.draw = draw
      self.weight = weight
      self.sire = sire
      self.dam = dam
      self.jockey = jockey
      self.score = score

def transformUserInputToDataModel():
   pass


def getHorseFinishTime(horse: Horse, distance, race_class, month, location, ml_model):

    'horse_color', 'horse_age', 'race_class', 'weight', 'dr', 'jockey', 'distance', 'month', 'horse_sire', 'horse_dam', 'no_of_turns'

    data = pd.DataFrame({
        'horse_color': [horse.color],
        'horse_age': [horse.age],
        'race_class': [race_class],
        'weight': [horse.weight],
        'dr': [horse.draw],
        'jockey': [horse.jockey],
        'distance': [distance],
        'month': [month], 
        'horse_sire': [horse.sire],
        'horse_dam': [horse.dam],
        'location': [location],
    })

    fieldsToEncodeWithMedian = [ 'jockey',
                                 'horse_color',
                                'horse_sire', 'horse_dam']
    for f in fieldsToEncodeWithMedian:
      data[f] = horse_history.encodeWithMedianRank(data[f], f)
    
    horse_history.applyNoOfTurns(data)
    predict_data = data.drop(columns=['location'], axis=1)
    print(predict_data)
    speed = ml_model.predict(predict_data)
    time = distance / speed
    return time
    

def getFeatureOptions(feature_name):
  if feature_name == "race_class":
    return ['1', '2', '3', '3R', '4', '4R', '4YO', '5', 'G1', 'G2', 'G3', 'GRIFFIN']
  #  elif feature_name == "G":
  #     return ['F', 'GF', 'G', 'GY', 'Y', 'YS', 'S', 'H', 'FT', 'GD', 'SL', 'WE', 'WS', 'WF']
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

  # Create the Dash app
  app = dash.Dash(__name__)

  colors = {
      "background": "#fff",
      "title": "#1d1d1f",
      "text": "#1d1d1f",
      "button_color": "#fff",
      "button_border_color": "transparent"
  }

  widths = {
      "dropdown_width": "200px",
      "input_width": "250px",
      "button_width": "100px"
  }

  heights = {
      "input_height": "32px",
      "button_height": "36px"
  }

  # Define the layout
  app.layout = html.Div(
      style={"backgroundColor": colors["background"], "fontFamily": "Arial"},
      children=[
          html.H1(
              children="HKJC Prediction",
              style={
                  "textAlign": "center",
                  "color": colors["title"]
              }
          ),

          html.Div(children=[
              html.H2(
                  children="Race",
                  style={
                      "textAlign": "center",
                      "color": colors["title"],
                  }
              ),
              html.Div(children=[
                  html.Div([
                      html.Div(children=[
                          html.Label("Race Class", style={"color": colors["text"]}),
                          dcc.Dropdown(
                              id="race_class_dropdown",
                              options=race_class_options,
                              value=race_class_options[0],
                              style={"width": widths["dropdown_width"]}
                          ),

                          html.Br(),
                          html.Label("Month", style={"color": colors["text"]}),
                          html.Br(),
                          dcc.Input(
                              id="month_input",
                              placeholder="Input race month",
                              type="number",
                              value=datetime.datetime.now().month,
                              min=1,
                              max=12,
                              step=1,
                              style={"width": widths["input_width"], "height": heights["input_height"]}
                          ),

                      ]),
                  ], style={"padding": 10, "flex": 1}),

                  html.Div([
                      html.Div(children=[
                          html.Label("Distance", style={"color": colors["text"]}),
                          html.Br(),
                          dcc.Dropdown(
                              id="distance_dropdown",
                              options=distance_options,
                              value=distance_options[0],
                              style={"width": widths["dropdown_width"]}
                          )
                      ]),
                  ], style={"padding": 10, "flex": 1}),

                  html.Div([
                      html.Div(children=[
                          html.Label("Location", style={"color": colors["text"]}),
                          dcc.Dropdown(
                              id="location_dropdown",
                              options=location_options,
                              value=location_options[0],
                              style={"width": widths["dropdown_width"]}
                          ),
                      ])
                  ], style={"padding": 10, "flex": 1}),
              ], style={"display": "flex", "flexDirection":"row", "backgroundColor": "#fafafc"}),

              html.Br(),
              html.H2(
                  children="Horse",
                  style={
                      "textAlign": "center",
                      "color": colors["title"],
                      "backgroundColor": "#fafafc"
                  }
              ),
              html.Div(children=[

                  html.Div(children=[
                      html.Label("Color", style={'color': colors["text"]}),
                      dcc.Dropdown(
                        id="horse_color_dropdown",
                        options=horse_color_options,
                        value=horse_color_options[0],
                        style={"width": widths["dropdown_width"]}
                      ),

                      html.Br(),
                      html.Label("Weight", style={'color': colors["text"]}),
                      html.Br(),
                      dcc.Input(
                          id="horse_weight_input",
                          placeholder="Input horse weight in pounds (900 - 1600)",
                          type="number",
                          value=1000,
                          min=900,
                          max=1600,
                          step=1,
                          style={"width": widths["input_width"], "height": heights["input_height"]}
                      ),

                      html.Br(),
                      html.Label("Jockey", style={'color': colors["text"]}),
                      html.Br(),
                      dcc.Input(
                          id="jockey_input",
                          placeholder="Input jockey in English",
                          type="text",
                          pattern=r'^[a-zA-Z0-9 ]*$',
                          style={"width": widths["input_width"], "height": heights["input_height"]}
                      ),


                  ], style={"padding": 10, "flex": 1}),

                  html.Div(children=[
                      html.Label("Age", style={'color': colors["text"]}),
                      dcc.Dropdown(
                        id="horse_age_dropdown",
                        options=horse_age_options,
                        value=horse_age_options[0],
                        style={"width": widths["dropdown_width"]}
                      ),
                     
                      html.Br(),
                      html.Label("Horse Sire", style={'color': colors["text"]}),
                      html.Br(),
                      dcc.Input(
                          id="horse_sire_input",
                          placeholder="Input horse sire in English",
                          type="text",
                          pattern=r'^[a-zA-Z0-9 ]*$',
                          style={"width": widths["input_width"], "height": heights["input_height"]}
                      ),
                  ], style={"padding": 10, "flex": 1}),

                  html.Div(children=[

                      
                      html.Label("Draw", style={'color': colors["text"]}),
                      dcc.Dropdown(
                        id="horse_dr_dropdown",
                        options=dr_options,
                        value=dr_options[0],
                        style={"width": widths["dropdown_width"]}
                      ),

                      html.Br(),
                      html.Label("Horse Dam", style={'color': colors["text"]}),
                      html.Br(),
                      dcc.Input(
                          id="horse_dam_input",
                          placeholder="Input horse dam in English",
                          type="text",
                          pattern=r'^[a-zA-Z0-9 ]*$',
                          style={"width": widths["input_width"], "height": heights["input_height"]}
                      ),
                  ], style={"padding": 10, "flex": 1}),
              ], style={"display": "flex", "flexDirection":"row", "backgroundColor": "#fafafc"}),

              html.Div(children=[
                  html.Button("Add Horse",
                      id="add_horse_button",
                      n_clicks=0,
                      style={"width": widths["button_width"],
                              "height": heights["button_height"],
                              "background": "#0071e3",
                              "color": "#fff",
                              "border-color": "transparent",
                              "border-radius": "8px",
                              "margin-right": "20px",
                      }),
                  html.Button("Clear",
                      id="clear_button",
                      n_clicks=0,
                      style={"width": widths["button_width"],
                              "height": heights["button_height"],
                              "background": "transparent",
                              "color": "#333",
                              "border": "1px solid #d6d6d6",
                              "border-radius": "8px",
                              }),
              ], style={"textAlign": "center"}),
          ], style={"backgroundColor": "#fafafc", "padding": "20px"}),
        

          html.Br(),
          html.H2(
              children="Result",
              style={
                  "textAlign": "center",
                  "color": colors["title"]
              }
          ),
          html.Div(id="output_label", style={"white-space":"pre-wrap", "textAlign": "center"})
      ]
  )

  output_horse_list = []

  # horse = Horse("Class A", "Imported", "Gelding", "John Smith", 2400, "New York", "July", "DamHorse")
  # print(horse.race_class)
  # print(horse.jockey)

  # Define the callback function for updating the graph
  @app.callback(
    dash.dependencies.Output('output_label', 'children'),
    [dash.dependencies.Input('race_class_dropdown', 'value'),
    dash.dependencies.Input('distance_dropdown', 'value'),
    dash.dependencies.Input('location_dropdown', 'value'),
    dash.dependencies.Input('month_input', 'value'),
    dash.dependencies.Input('horse_color_dropdown', 'value'),
    dash.dependencies.Input('horse_age_dropdown', 'value'),
    dash.dependencies.Input('horse_weight_input', 'value'),
    dash.dependencies.Input('horse_dr_dropdown', 'value'),
    dash.dependencies.Input('jockey_input', 'value'),
    dash.dependencies.Input('horse_sire_input', 'value'),
    dash.dependencies.Input('horse_dam_input', 'value'),
    dash.dependencies.Input('add_horse_button', 'n_clicks'),
    dash.dependencies.Input('clear_button', 'n_clicks'),
    ],
    [dash.dependencies.Input('output_label', 'children')]
  )
  def update_output(selected_race_class, selected_distance, selected_location, selected_month, selected_color, selected_age, selected_weight, selected_dr, selected_jockey, selected_sire, selected_dam, add_clicks, clear_clicks, previous_output):
      msg = "No horse"
      if "add_horse_button" == ctx.triggered_id:
        horse = Horse(selected_color, selected_age, selected_dr, selected_weight, selected_sire, selected_dam, selected_jockey, 1)
        predict_finishtime = getHorseFinishTime(horse, selected_distance, selected_race_class, selected_month, selected_location, model)
        horse.score = predict_finishtime
        output_horse_list.append(horse)
        msg = ""
        for index, output_horse in enumerate(output_horse_list):
          msg += f"Horse color {output_horse.color} score: {output_horse.score}\n"
      elif "clear_button" == ctx.triggered_id:
        output_horse_list.clear()
        msg = "Clear horse"
      return html.Div(msg)


      # selected_distance_km = selected_distance.astype("int") / 1000
      # Retrieve stock data
      # x_data = [[selected_race_class, selected_import_type, selected_g, selected_distance_km, selected_age, selected_g, selected_import_type]]
      # Create the pandas DataFrame
      # df = pd.DataFrame(x_data, columns=['distance', 'horse_age', 'G', 'horse_import_type'])
      # output_result = model.predict(df)
      # return html.Label(f"Y result: {output_result}")

  # Run the app
  # if __name__ == '__main__':
  app.run_server(debug=True)
