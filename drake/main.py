import pandas as pd
from dash import Dash, Output, Input, State, ClientsideFunction

from drake.functions import *

pd.options.mode.chained_assignment = None

rng = np.random.default_rng()

cols_count = 30
columns = ['col_' + str(i) for i in np.arange(1, cols_count + 1)]
data = rng.integers(0, 100, size=(100, cols_count))
df = pd.DataFrame(data, columns=columns)

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, ],
           external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.js",
                             'https://code.jquery.com/jquery-3.2.1.min.js'],
           )

settings = settings_container(df.columns)
col_defs, table = table_factory(df)

app.layout = dbc.Container(
    children=[settings, table, html.Div(id='result')],

    style={'width': '85%', 'height': '100vh'},
    fluid=True,

)

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output("drag_container", "data-drag"),
    [Input("drag_container", "id")],
    [State("drag_container", "children")],
)


@app.callback(
    Output('result', 'children'),
    Input('settings-apply-btn', 'n_clicks'),
    Input('drag_container', 'children'),
)
def settings_apply(n, children):
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)
