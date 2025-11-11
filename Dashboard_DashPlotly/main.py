from dash import Dash, html,callback, dash_table,dcc,Input,Output
import pandas as pd
import plotly.express as px


#organização dos dados
df = pd.read_csv('Fortaleza-Dengue.csv', delimiter = ',')
dff = df[['data_iniSE','casos']].sort_values(by='data_iniSE')
dff['data_iniSE'] = pd.to_datetime(dff['data_iniSE'])
dff['ano'] = dff['data_iniSE'].dt.year

#Inicialização
app = Dash(__name__)

# Requires Dash 2.17.0 or later
app.layout = html.Div(children=[
    html.H1(children='Estatísticas gerais - Infodengue'),
    html.H3(children='Municipio de Fortaleza'),
    html.Hr(),
    
    # DataTable espera lista de dicts -> use DataFrame.to_dict('records')
    dash_table.DataTable(dff[['data_iniSE','casos']].to_dict('records'), page_size=6),
    # Dropdown com opções no formato {'label','value'}
    dcc.Dropdown(
        id='ano',
        options=[{'label': int(y), 'value': int(y)} for y in sorted(dff['ano'].dropna().unique())],
        placeholder='Selecione o ano'
    ),

    dcc.Graph(id='serie',figure=px.line(dff, x='data_iniSE', y='casos')),


])

@callback(
    Output(component_id = 'serie', component_property='figure'),
    Input(component_id='ano', component_property='value')
)
def update_graph(ano):
    if ano is None:
        df_plot = dff.copy()
        title = 'Casos por data (todos os anos)'
    else:
        df_plot = dff[dff['ano']==ano].copy()
        title = f"Casos de {ano}"
 
    # agrega por data (soma casos por dia) e plota
    df_soma = df_plot.groupby('data_iniSE', as_index=False)['casos'].sum()
    fig = px.line(df_soma, x='data_iniSE', y='casos', title=title)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)