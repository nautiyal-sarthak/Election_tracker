import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import json
import pandas as pd
import plotly.express as px


## Importing data
with open(
        '/Users/sarthaknautiyal/PycharmProjects/election-analytics/electionAnalytics/electionAnalytics/spiders/constituencywise.json',
        'r') as f:
    data = json.load(f)
constituencywise_df = pd.DataFrame(data)
constituencywise_df["margin"] = pd.to_numeric(constituencywise_df["margin"])

with open(
        '/Users/sarthaknautiyal/PycharmProjects/election-analytics/electionAnalytics/electionAnalytics/spiders/RoundwiseResults.json',
        'r') as f:
    data = json.load(f)
roundwise_df = pd.DataFrame(data)
roundwise_df["total"] = pd.to_numeric(roundwise_df["total"])
roundwise_df["round"] = pd.to_numeric(roundwise_df["round"])

## Creating all the data sets
constituencywise_df.sort_values('margin', inplace=True, ascending=True)
constituencywise_df.reset_index(inplace=True)
summary = constituencywise_df[["status", "leadingParty", "margin"]].groupby(
    ["status", "leadingParty"]).count().reset_index()
closeFights = constituencywise_df[
    ['constituency', 'leadingParty', 'trailingParty', 'margin', 'status', 'last_winning_party', 'last_margin']]

# latestrounds
roundwise_df['rank'] = roundwise_df.groupby(['seat'])['round'].rank(method='dense', ascending=False)
last_round_df = roundwise_df[roundwise_df['rank'] == 1]

# vote share at seat level
voteShare_df = last_round_df.groupby(['party'])['total'].sum()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    html.H1(children='Election Tracker'),
    html.Div(children='''
       A POC
   '''),
html.Div([
        html.Div([
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': summary[summary["status"] == "Result Declared"]['leadingParty'],
                        'y': summary[summary["status"] == "Result Declared"]['margin'],
                        'type': 'bar',
                        'name': "Win"
                    },
                        {
                            'x': summary[summary["status"] != "Result Declared"]['leadingParty'],
                            'y': summary[summary["status"] != "Result Declared"]['margin'],
                            'type': 'bar',
                            'name': "Lead"
                        }
                    ],
                    'layout': dict(
                        title='Seat Summary (Leads + Win)',
                        showlegend=True,
                        barmode='stack'
                    )
                }
            )
        ], className="six columns"),

        html.Div([
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'values': voteShare_df,
                        'type': 'pie',
                        'labels': voteShare_df.index
                    }
                    ],
                    'layout': dict(
                        title='Vote Share',
                        showlegend=False
                    )
                }
            )
        ], className="six columns"),
    ], className="row")
    , html.H3(children='Constituency wise Trends'),
    html.Div(children='''
       Select a Constituency to get more details
   '''),
    html.Br(),
    dash_table.DataTable(
        id='table-filtering',
        data=closeFights.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in closeFights.columns],
        fixed_rows={'headers': True, 'data': 0},
        row_selectable='single',
        style_table={
            'maxHeight': '300px',
            'overflowY': 'scroll',
            'border': 'thin lightgrey solid'
        },
        style_cell={'textAlign': 'left','maxWidth': 0},
        style_header={
        'backgroundColor': 'lightblue',
        'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },{
            'if': {
                'column_id': 'last_margin',
                'filter_query': '{last_margin} > {margin}'
            },
            'backgroundColor': 'red',
            'color': 'white',
        },{
            'if': {
                'column_id': 'margin',
                'filter_query': '{last_margin} < {margin}'
            },
            'backgroundColor': 'green',
            'color': 'white',
        }]
    ,
        filter_action='native'
    )
    , 'Number of rows : ',
    dcc.Dropdown(
        id='loading-states-table-prop',
        options=[
            {'label': x, 'value': x}
            for x in range(1, closeFights.index.size)
        ],
        value='8'
    )
    ,
    html.Div(id='datatable-row-ids-container')
])

#
# @app.callback(
#     [Output("progress", "value"), Output("progress", "children")],
#     [Input("progress-interval", "n_intervals")]
# )
# def update_progress(n):
#     # check progress of some background process, in this example we'll just
#     # use n_intervals constrained to be in 0-100
#     progress = min(n % 110, 100)
#     # only add text after 5% progress to ensure text isn't squashed too much
#     return progress, progress if progress >= 5 else ""

@app.callback(
    Output('datatable-row-ids-container', 'children'),
    [Input('table-filtering', 'selected_rows')])
def update_graphs(selected_rows):
    if selected_rows != None:
        selected_constituency_data = closeFights.loc[selected_rows]
        selected_constituency = selected_constituency_data['constituency'].iloc[0]
        constituency_data = roundwise_df[roundwise_df['seat'] == 'NCT OF Delhi-' + str(selected_constituency)]
        last_round_contituency = last_round_df[last_round_df['seat'] == 'NCT OF Delhi-' + str(selected_constituency)]
        last_round_contituency_voteshare = last_round_contituency.groupby(['party'])['total'].sum()

        fig = px.line(dict(candidate=constituency_data['candidate'], votes=constituency_data['total'],
                           round=constituency_data['round'], party=constituency_data['party']),
                      x='round', y='votes', color='party', line_group='candidate', title='Round-by-Round comparison')
        fig.update_traces(mode='markers+lines')

        return [html.H3(children='Trends for ' + selected_constituency),
            dcc.Graph(
                id=selected_constituency + '--row-ids',
                figure=fig
            ),
            dcc.Graph(
                id=selected_constituency + 'graph-2-tabs_vote',
                figure={
                    'data': [{
                        'values': last_round_contituency_voteshare,
                        'type': 'pie',
                        'labels': last_round_contituency_voteshare.index
                    }
                    ],
                    'layout': dict(
                        title='Vote Share for ' + selected_constituency,
                        showlegend=True
                    )
                }
            )

        ]


if __name__ == '__main__':
    app.run_server(debug=True)
