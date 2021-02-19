import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px
import json
import argparse

def create_app(inpath):
    df=pd.read_csv(inpath,sep='\t',names=['datetime','module','level','message'],parse_dates=['datetime'])

    df_e=df[(df.module=='http.client')&(df.message.str.startswith('reply'))].copy()
    isPOST=df.message.str.contains('POST')
    isGET =df.message.str.contains('GET' )
    df_s=df[(df.module=='http.client')&(df.message.str.startswith('send:'))&(isPOST|isGET)].copy()
    df_d=df[(df.module=='http.client')&(df.message.str.startswith('send: b\'{'))].copy()

    df_s['route']=df_s.message.str.extract(r'(GET|POST) /([a-zA-Z]+)')[1]
    df_d['data']=df_d.message.str.extract(r"send: b'(\{.*\})'")

    df_t=df_s.reset_index().merge(df_e.reset_index(),left_index=True,right_index=True,suffixes=('_start','_end'))
    df_t=df_t.merge(df_d[['data']].reset_index(), left_index=True, right_index=True, suffixes=('','_data'))

    df_t['idx']=df_t.index
    df_t['module']='http.client'
    df_t['duration']=df_t['datetime_end']-df_t['datetime_start']
    df_t['start']=df_t['datetime_start']-df_t['datetime_start'].min()

    testfig = px.timeline(df_t, x_start='datetime_start', x_end='datetime_end', y='module', color='route', custom_data=['idx'], hover_data=['route','duration'])
    testfig.update_layout(clickmode='event+select')

    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = dbc.Container(children=[
        html.Div(children=[html.B("Viewing: "),inpath]),
        dcc.Graph(id='timeline', figure=testfig),
        dbc.ListGroup(id='timeline_selected')
        ])

    @app.callback(
        Output('timeline_selected', 'children'),
        Input('timeline', 'selectedData'))
    def display_selected_data(selectedData):
        if selectedData is None:
            return []

        result=[]
        for point in selectedData['points']:
            idx=point['customdata'][0]
            df_item=df_t.loc[idx]

            result.append(dbc.ListGroupItem([
                html.H5(df_item.route),
                html.Ul([
                    html.Li([
                        html.Label('Start:'),
                        ' {} s'.format(df_item.start.total_seconds())
                        ]),
                        html.Li([
                            html.Label('Duration:'),
                            ' {} s'.format(df_item.duration.total_seconds())
                            ])
                    ]),
                html.H6('Data'),
                html.Pre(json.dumps(json.loads(df_item.data), indent=2))
                ]))
        return result
    return app
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple visualizer for httptime data.")
    parser.add_argument('inpath'                             , help='Path to httptime output.')
    parser.add_argument('-p','--port', type=int, default=5000, help='Port for web server.')

    args = parser.parse_args()

    app=create_app(args.inpath)
    app.run_server(port=args.port, debug=True)
