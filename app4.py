
import plotly.graph_objs as go
import pandas as pd

import dash_core_components as dcc
import dash
import dash_html_components as html
from QUANTAXIS.QAUtil import QASETTING


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

myclient = QASETTING.client
database = myclient.mydatabase
col = database.prediction
x = col.find()
outcome = pd.DataFrame(list(x))
outcome = outcome.drop(columns = '_id')
outcome['datetime'] = pd.to_datetime(outcome['datetime'])
outcome.set_index('datetime', inplace=True)
data = outcome

# data = pd.read_csv('./prediction.csv',
#                    index_col=0)


prediction = go.Scatter(
    x=data.index,
    y=data['predict'],
    name="Predicted Value",
    line=dict(color='#17BECF'),
    opacity=0.8)

actualtraffic = go.Scatter(
    x=data.index,
    y=data['y'],
    name="Actual Value",
    line=dict(color='#7F7F7F'),
    opacity=0.8)

fig = go.Figure(
    data=[prediction, actualtraffic],
    layout=go.Layout(
        title='',
    )
)

fig.update_layout(
    xaxis=go.layout.XAxis(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

app.layout = html.Div(children=[
    html.H1(children='Forecasting Result'),
    dcc.Graph(
        figure=fig
    )
])


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=808, debug=True)


