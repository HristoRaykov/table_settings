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
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"],
           )

table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]

row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")], id='row1')
row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")], id='row2')
row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")], id='row3')
row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")], id='row4')

table_body = [html.Tbody([row1, row2, row3, row4], id="drag_container")]

table = dbc.Table(table_header + table_body, bordered=True)

modal = dbc.Modal([dbc.ModalHeader(close_button=True),
                   dbc.ModalBody([table], ),
                   dbc.ModalFooter([dbc.Button('Apply',
                                               id='settings-apply-btn',
                                               size='sm', color='secondary', outline=True,
                                               )], style={'justify-content': 'center', }),
                   ],
                  id='settings-modal',
                  # keyboard=False,
                  # scrollable=True,
                  # backdrop=False,
                  is_open=False,
                  # centered=True,
                  # size="md",
                  # class_name
                  # style={'width': 380, },
                  )

# app.layout = dbc.Container(
#     children=[
#         dbc.Button('Apply',
#                    id='settings-apply-btn',
#                    size='sm', color='secondary', outline=True,
#                    ),
#         table,
#         html.Div(id='result'),
#     ],
#     style={'width': '100%', 'height': '100vh'},
#     fluid=True,
# )

app.layout = dbc.Container(
    children=[
        dbc.Button('Settings',
                   id='settings-modal-open-btn',
                   size='sm', color='secondary', outline=True,
                   ),
        modal,
        html.Div(id='result'),
    ],
    style={'width': '100%', 'height': '100vh'},
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
    Input("drag_container", "children"),
    # State("drag_container", "children"),
)
def settings_apply(n, children):
    return ''


@app.callback(
    Output('settings-modal', 'is_open'),
    [Input('settings-modal-open-btn', 'n_clicks'), ],  # Input('settings-modal-close-btn', 'n_clicks')
    [State('settings-modal', 'is_open')],
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
