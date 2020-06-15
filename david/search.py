import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='dAvId'),

    html.Div(children='''
        A decentralized search engine powered by AI.
    '''),

    html.Div(children=[
        dcc.Input(id='input-box', type='text'),
        html.Button('Search', id='button')
        ]),

    html.Div(id='output-container-button',
             children='Enter a value and press submit'),

])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=5000)
