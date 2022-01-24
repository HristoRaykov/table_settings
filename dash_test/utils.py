import numpy as np
from dash_test import dash_table
from dash_test.dash_table.Format import Align

ID_SEP = '-'


def find_element_by_id(children, id):
    if isinstance(children, dict):
        children_list = [children]
    else:
        children_list = children

    for child in children_list:
        if isinstance(child, dict):
            props = child.get('props')
            if props is not None:
                el_id = props.get('id')
                if el_id == id:
                    return child

            chldren = props.get('children')
            if chldren:
                chld = find_element_by_id(chldren, id)
                if chld:
                    return chld

    return None


def generate_id(*args):
    arguments = [arg for arg in args if arg is not None]
    id = ID_SEP.join(arguments)

    return id


def column_definitions(df):
    col_defs = dict()
    for col in df.columns:
        t = df[col].dtype
        if t == np.float64:
            col_def = dict(id=col, name=col, type='numeric',  # hideable=True,
                           format=dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed).group(
                               True))
        elif t == np.int64:
            col_def = dict(id=col, name=col, type='numeric',  # hideable=True,
                           format=dash_table.Format.Format(align=Align.right).group(True))
        elif np.issubdtype(t, np.datetime64):
            col_def = dict(id=col, name=col, type='datetime',  # hideable=True,
                           format=dash_table.Format.Format(align=Align.center))
        else:
            col_def = dict(id=col, name=col, type='text',  # hideable=True,
                           format=dash_table.Format.Format(align=Align.left))

        col_defs[col] = col_def

    return col_defs


def _is_enum_col(series):
    val_counts = series.value_counts()

    if val_counts.empty:
        return False

    if val_counts.values[0] > 1:
        return True
    else:
        return False
