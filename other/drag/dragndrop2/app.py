import dash_test
import dash_html_components as html
from dash_test.dependencies import Input, Output, ClientsideFunction, State

app = dash_test.Dash(
    __name__,
    external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"],
)

app.layout = html.Div(
    id="main",
    children=[
        html.Button(id="btn", children="Refresh display for order of children"),
        html.Label(id="order"),
        html.Div(
            id="drag_container",
            className="container",
            children=[html.Button(id=f"child-{i}", children=f"child-{i}") for i in range(5)],
        ),
    ],
)

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output("drag_container", "data-drag"),
    [Input("drag_container", "id")],
    [State("drag_container", "children")],
)


@app.callback(
    Output("order", "children"),
    [
        Input(component_id="btn", component_property="n_clicks"),
        Input(component_id="drag_container", component_property="children"),
    ],
)
def watch_children(nclicks, children):
    """Display on screen the order of children"""
    return ", ".join([comp["props"]["id"] for comp in children])


if __name__ == "__main__":
    app.run_server(debug=True)