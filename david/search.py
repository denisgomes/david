import dash
import dash_core_components as dcc
import dash_html_components as html

from indexer import Indexer


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='dAvId'),

    html.Div(children='''
        A decentralized search engine powered by AI.
    '''),

    html.Div(children=[
        dcc.Input(id='input-box', type='text'),
        html.Button('Search', id='button', n_clicks=0)
        ]),

    html.Div(id='document-list',
             children=[])
])


@app.callback(
    dash.dependencies.Output('document-list', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')],
    )
def update_output(n_clicks, value):
    indexer = Indexer()
    results = indexer.search(value)

    li_children = []
    for no, result in enumerate(results, 1):
        url, title, snippet = result

        if title:
            li = html.Li(children=[
                                html.A(title, href=url),
                                dcc.Markdown(children=snippet),
                            ])

            li_children.append(li)

    ol = html.Ol(children=li_children)

    return ol


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=5000)
