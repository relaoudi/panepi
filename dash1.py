#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import base64
import dash_bootstrap_components as dbc
from collections import OrderedDict
from dash.dash_table.Format import Format, Scheme, Trim
from dash.dash_table import FormatTemplate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_auth


# In[2]:


today=datetime.datetime.today()
today


# In[3]:


# Incorporate data
df = pd.read_excel('TableauxBord.xlsx',skiprows=2)
df


# In[4]:



df1=df.groupby("Région").sum()
df1.reset_index(inplace=True)
a=df1.loc[11]
df1.loc[11]=df1.loc[12]
df1.loc[12]=a
df1.insert(0,"Id",[i for i in np.arange(len(df1))],True)
df1


# In[5]:


df1=df1[df1.columns[[i for i in np.arange(12)]]]

df1


# In[6]:


df1.columns


# In[7]:


t_eng=df1["Taux d'Engagement"]=df1["Cout de Projets Engagés"]/df1['Cout des Projets  MDH TTC']
t_ach=df1["Taux d'Achevement"]=df1["Cout de Projets Achevés"]/df1['Cout des Projets  MDH TTC']
df1


# In[8]:


total=df1['Cout des Projets  MDH TTC'].iloc[-1]
total


# In[9]:


acheve=df1['Cout de Projets Achevés'].iloc[-1]


# In[10]:


encours=df1['Cout de Projets Encours'].iloc[-1]


# In[11]:


programme=df1['Cout de Projets Programmés'].iloc[-1]


# In[12]:


engage=acheve+encours
totalach=total-acheve
totaleng=total-engage


# In[13]:


indicat=pd.DataFrame({'red':['red1','red2'],'eng':[totaleng,engage],'ach':[totalach,acheve]})
indicat


# In[14]:


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
    
                  
               # }).update_traces(hoverinfo='skip',textinfo = 'text', 
 
fig2.show()



# In[15]:


#color_discrete_map={'red1':'#FFFFE6','red2':'#FF00D4'},
colors = ['white', 'FF00D4']
fig3=px.pie(indicat,names='red',values='ach',color='red', opacity= 0.7,
                    
                        hole = .7
                    
           ).update_layout(#plot_bgcolor = 'skyblue',
            paper_bgcolor = 'skyblue',          
            #margin = dict(t = 35, b = 10, r = 0, l = 0),
            hovermode=False,
            showlegend = False,
            title={'text': "Taux d'Achévement",
                   #'font':{'size':10},
                   'y': 0.85,
                   'x': 0.5,
                   #'xanchor': 'center',
                   #'yanchor': 'top'
                  }).update_traces(textinfo = 'text', 
                        marker = dict(colors = colors,line=dict(color='darksalmon', width=0.5)))

fig3.show()


# In[16]:


df1["Taux d'Achevement"].iloc[-1]


# In[17]:


df1.index


# In[18]:


#pour les donut chart


# In[19]:


#for i in np.arange(2,12):
  #  if df1.dtypes[i] == 'float64':
    #    df1.iloc[:, i] = df1.iloc[:, i].map('{:,.2f}'.format)
   # elif df.dtypes[i] == 'int64':
      #  df1.iloc[:, i] = df1.iloc[:, i].map('{:,.0f}'.format)
#for i in [12,13] :
# df1.iloc[:, i] = df1.iloc[:, i].map('{:,.2%}'.format)
    
       


# In[20]:


df1.columns


# In[21]:


with open('image_gauche1.jpg', "rb") as image_file1:
    img_data1 = base64.b64encode(image_file1.read())
    img_data1 = img_data1.decode()
    img_data1= "{}{}".format("data:image/jpg;base64, ", img_data1)

with open('image_droite1.jpg', "rb") as image_file2:
    img_data2 = base64.b64encode(image_file2.read())
    img_data2 = img_data2.decode()
    img_data2 = "{}{}".format("data:image/jpg;base64, ", img_data2)   


# In[22]:


percentage = FormatTemplate.percentage(0)


# In[23]:


#Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],prevent_initial_callbacks=True)
server=app.server

# In[25]:


auh=dash_auth.BasicAuth(
app,
{'redouane':'1234',
'housni':'2341',
'boukra':'3412'})


# In[26]:


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
    #'position':'absolute'
    
  # 'width':60, 'height': 60,'position':'relative' 
    #taux achevement
    html.Div(children=[
       html.Div(children=[dcc.Graph(id = 'donut_chart1',
                          config = {'displayModeBar': False},
                         figure=fig2,
                     style={'height':'100%','width':'100%'},className='dash-graph')],className='dash-center',
            style= {'position':'absolute'}),
                # style={'width': '0%', 'height': 'auto', 'margin': 'auto'}),
        
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
                 #style={'width': '5%', 'height':'auto', 'margin': 'auto'})],
                             
                 
               #    'position':'absolute','margin-top': '50%','margin-left': '50%'
             #  }))]
        style={'display':' flex','justify-content': 'center','align-items':'center',
                     'width': '100%', 'height': 100, 'margin-bottom':5,'backgroundColor':'#E6FBFF'}),
        
                # style={'width': '100%', 'height': '100%', 'margin': 'auto'},className='dash-fullscreen'),
                
        
           # style={'height':500,'width':'100%','backgroundColor':'red','display':'flex',
                  # 'justify-content': 'center'}),
    
    #, 'align-items':'center'
              #  html.Div( html.P(f"{t_ach.iloc[-1]:,.0%}",
             # style ={
               #    'color': '#FF00D4',
                #  'fontSize': 25,
                #  'font-weight': 'bold',
               #    'position':'absolute','margin-top': '50%','margin-left': '50%'
             #  }))],
        #),
            #style={'position':'relative', "width":'50%'})             
              #style={'display':' flex','flex-direction': 'row','margin-left':'50%','margin-top':'50%'})],           
                       #  style={'display':' flex','flex-direction': 'row','position': 'absolute','margin-top': 30})]
               
                        # style={ 'display': 'flex','flex-wrap':' wrap', 'justify-content': 'center','margin-top': 10,'gap': 10}),
    

                                       
     html.Div(className='row',children=[
         html.Div(dash_table.DataTable(id='datatable-interactivity',data=df1.to_dict('records'),
         columns=[dict(name=i, id=i ,type='numeric',format=percentage,deletable=True,selectable= True)
                  if i in df1.columns[[12,13]]
                  else dict(name=i, id=i ,type='numeric',deletable=True,selectable= True,format=Format( precision=0,scheme=Scheme.fixed, trim=Trim.yes))
                  for i in df1.columns
                 
                 ],
                  #format=Format( precision=2,scheme=Scheme.fixed, trim=Trim.yes)],    
        
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_header={ 'backgroundColor': 'rgb(204,230,255)', 'color': 'black' },
        #style_data={'backgroundColor': 'rgb(50, 50, 50)','color': 'white','format':Format(precision=2,scheme=Scheme.fixed, trim=Trim.yes for i in df1.columns)},                                                                                             
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



# In[27]:


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
           Input('datatable-interactivity', 'selected_columns'))
    
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# In[ ]:



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
                                                                 )#.update_traces(marker_color=px.colors.qualitative.Alphabet))
                     )]                    

#def update_graph(col_chosen):
    #fig = px.histogram(df1, x='Région', y=col_chosen, histfunc='sum')
    #return fig

@app.callback(
    Output("Télécharger-Renforcement&Securisation", "data"),
    Input("btn-download-Renf&Secur", "n_clicks"),
    prevent_initial_call=True
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_excel, "Renf&Secur.xlsx", sheet_name="Renforcement & Sécurité")
   

# Run the app
if __name__ == '__main__':
    app.run_server()


# In[ ]:





# In[ ]:





# In[ ]:




