
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import datetime
import plotly.express as px
import dash_bootstrap_components as dbc
import base64
from dash.dash_table.Format import Format, Scheme, Trim
from dash.dash_table import FormatTemplate
import plotly.graph_objects as go


today=datetime.datetime.today()

df = pd.read_excel('TableauxBord.xlsx',skiprows=2)
df1=df.groupby("Région").sum()
df1.reset_index(inplace=True)
a=df1.loc[11]
df1.loc[11]=df1.loc[12]
df1.loc[12]=a
df1.insert(0,"Id",[i for i in range(len(df1))],True)

t_eng=df1["Taux d'Engagement"]=df1["Cout de Projets Engagés"]/df1['Cout des Projets  MDH TTC']
t_ach=df1["Taux d'Achevement"]=df1["Cout de Projets Achevés"]/df1['Cout des Projets  MDH TTC']

total=df1['Cout des Projets  MDH TTC'].iloc[-1]
acheve=df1['Cout de Projets Achevés'].iloc[-1]
encours=df1['Cout de Projets Encours'].iloc[-1]
programme=df1['Cout de Projets Programmés'].iloc[-1]

engage=acheve+encours
totalach=total-acheve
totaleng=total-engage

indicat=pd.DataFrame({'red':['red1','red2'],'eng':[totaleng,engage],'ach':[totalach,acheve]})

labels = indicat['red']
values = indicat['ach']
colors = ['white', 'FF00D4']
trace = go.Pie(labels=labels, values=values, marker = dict(colors = colors,
                                      line=dict(color='black', width=0.5)),
                        hoverinfo = 'skip',
                        textinfo = 'text',
                        hole = .7,
                        rotation = 90
                        )
layout = go.Layout(autosize=False,
    width=150,
    height=100,
       margin=go.layout.Margin(
        l=5,
        r=5,
        b=5,
        t=20,
        pad = 0.2
    ),            
           plot_bgcolor = 'rgba(0,0,0,0)',
            paper_bgcolor = 'rgba(0,0,0,0)',
            showlegend = False,
            title={'text':"Taux d'Achévement",
                   'y': 0.9,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont = {'color': 'black',
                         'size': 12}
        )
fig2=go.Figure(data=[trace], layout=layout)    

with open('image_gauche1.jpg', "rb") as image_file1:
    img_data1 = base64.b64encode(image_file1.read())
    img_data1 = img_data1.decode()
    img_data1= "{}{}".format("data:image/jpg;base64, ", img_data1)

with open('image_droite1.jpg', "rb") as image_file2:
    img_data2 = base64.b64encode(image_file2.read())
    img_data2 = img_data2.decode()
    img_data2 = "{}{}".format("data:image/jpg;base64, ", img_data2)   

percentage = FormatTemplate.percentage(0)

 #Initialize the app - incorporate css
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],prevent_initial_callbacks=True)

app.layout = html.Div(children=[
html.Div([html.Div(html.Img(src= img_data1,width=40,height=40),style={'float':'left'}),html.Div(html.Img(src= img_data2,width=40,height=40)
        ,style={'float':'right'}), html.Div([html.H1("Programme National pour l'Approvisionnement en Eau Potable et l'Irrigation 2020-2027",
                                                    style={'display':'inline-block','margin-right': 180,'color': 'white', 'fontSize': 25}),
                                             html.H2(f"{today: %B-%Y}",style={'display': 'inline-block','color': 'yellow', 'fontSize': 15})],
                                            style={'font-size': '0'}),
        ],
          style={'background-color': 'rgb(25,25,255)','width':'100%','height':40}),
    
    html.Div([
            html.H6(children='Renforcement & Sécurisation',
                    style={
                        'textAlign': 'center','color': 'black','background-color': 'rgb(204,230,255)','box-shadow': '5px 10px',
                  'font-weight': 'bold' ,'text-align': 'center' }
                    )],style={'fontSize':15,'height':20,'width':'40%','margin-left':'auto','margin-right':'auto',
                              'margin-bottom':5, 'border': '3px solid #4287f5'}),
    
     html.Div([
     html.Div([
            html.H6(children='Total Des Projets',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),

            html.P((f"{df1['Cout des Projets  MDH TTC'].iloc[-1]:,.0f} MDH").replace(","," "),
                   style={
                       'textAlign': 'center',
                       'color': '#FF00D4',
                       'font-weight': 'bold'
                       })
                 
     ], style={ 'float': 'left','height':50,'width':'22%','margin-left':20,'margin-right':20,'margin-top':5,'margin-bottom':5,
               'position':'relative','background-color': 'rgb(204,230,255)','box-shadow': '5px 10px',
               } ),
    html.Div([
            html.H6(children='Projets Achevés',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),

            html.P((f"{df1['Cout de Projets Achevés'].iloc[-1]:,.0f} MDH").replace(","," "),
                   style={
                       'textAlign': 'center',
                       'color': '#FF00D4',
                       'font-weight': 'bold'
                })
                   
    ], style={'float': 'left','height':50,'width':'22%','margin-left':20,'margin-right':20,'margin-top':5,'margin-bottom':5,
              'position':'relative','background-color': 'rgb(204,230,255)','box-shadow': '5px 10px',
              
                } ),
   # 'display':'inline-block'
     html.Div([
            html.H6(children='Projets En Cours',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),
     

            html.P((f"{df1['Cout de Projets Encours'].iloc[-1]:,.0f} MDH").replace(","," "),
                   style={
                       'textAlign': 'center',
                       'color': '#FF00D4',
                       'font-weight': 'bold'
                       })
        
                 
     ] ,style={ 'float': 'left','height':50,'width':'22%','margin-left':20,'margin-right':20,'margin-top':5,'margin-bottom':5,
              'position':'relative','background-color': 'rgb(204,230,255)',
               'box-shadow': '5px 10px',
                }),
         
    html.Div([
            html.H6(children='Projets Programmés',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),

            html.P((f"{df1['Cout de Projets Programmés'].iloc[-1]:,.0f} MDH").replace(","," "),
                   style={
                       'textAlign': 'center',
                       'color': '#FF00D4',
                       'font-weight': 'bold'
                       })
                
    ],  style={'float': 'left','height':50,'width':'22%',
               'margin-left':20,'margin-right':20,'margin-top':5,'margin-bottom':5,
               'position':'relative','background-color':'rgb(204,230,255)','box-shadow': '5px 10px',
              
            })],
         style={'fontSize':15,'height':60,'width':'100%'}),
 
    html.Div(children=[
       html.Div(children=[dcc.Graph(id = 'donut_chart1',
                          config = {'displayModeBar': False},
                         figure=fig2,
                     style={'height':'100%','width':'100%'},className='dash-graph')],className='dash-center',
            style= {'position':'absolute'}),
              
        html.Div(children= [html.P(f"{t_ach.iloc[-1]:,.0%}",
                         style ={
                       'fontSize': 15,
                       'font-weight': 'bold',
                       'height':'15%','width':'100%',
                        'textAlign': 'center' ,  
                        'color': '#FF00D4',
                       'margin-top':25}  ,
                                   className='dash-graph')],className='dash-center',
                    style= {'position':'absolute'})],        
                 
        style={'display':' flex','justify-content': 'center','align-items':'center',
                     'width': '100%', 'height': 100, 'margin-bottom':5,'backgroundColor':'#E6FBFF'}),
        
                                       
     html.Div(className='row',children=[
         html.Div(dash_table.DataTable(id='datatable-interactivity',data=df1.to_dict('records'),
         columns=[dict(name=i, id=i ,type='numeric',format=percentage,deletable=True,selectable= True)
                  if i in df1.columns[[12,13]]
                  else dict(name=i, id=i ,type='numeric',deletable=True,selectable= True,format=Format( precision=0,scheme=Scheme.fixed, trim=Trim.yes))
                  for i in df1.columns
                 
                 ],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_header={ 'backgroundColor': 'rgb(204,230,255)', 'color': 'black' },                                                                    
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="multi",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 13),
        style={'width': '60%', 'display': 'inline-block'}),
    html.Div(id='bar-container',style={'width': '40%', 'display': 'inline-block'})]),
    
    html.Div([
    html.Button("Télécharger", id="btn-download-Renf&Secur",
                style={'backgroundColor':'#E6FBFF','box-shadow': '5px 10px','margin-left': '90%'}),
    dcc.Download(id="Télécharger-Renforcement&Securisation")
    ])
])


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
           Input('datatable-interactivity', 'selected_columns'))
    
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('bar-container', 'children'),
    Input('datatable-interactivity', 'derived_virtual_data'),
    Input('datatable-interactivity', 'derived_virtual_selected_rows'),
    Input('datatable-interactivity', 'selected_columns'))


def update_graphs(data_rows, derived_virtual_selected_rows,cols):
  
    # Création du sous-tableau
    sub_df = pd.DataFrame(data_rows)#[cols] if rows is not None and cols is not None else pd.DataFrame(rows)
   # Création des données pour le graphique à barres
    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9' for i in range(len(sub_df))]
    return [
            dcc.Graph(id='bar-chart',figure=px.bar(sub_df, x='Région',y=cols,barmode='group', color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                  ).update_layout(legend=dict(yanchor="top", y=0.9, xanchor="left", x=0.2),xaxis={'categoryorder': 'total ascending'}
                                                                 )
                     )]                    

@app.callback(
    Output("Télécharger-Renforcement&Securisation", "data"),
    Input("btn-download-Renf&Secur", "n_clicks"),
    prevent_initial_call=True
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_excel, "Renf&Secur.xlsx", sheet_name="Renforcement & Sécurité")
   

# Run the app

