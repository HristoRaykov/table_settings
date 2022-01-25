import numpy as np
import pandas as pd

from table_settings.constants import ID_SEP


def generate_id(*args):
    arguments = [arg for arg in args if arg is not None]
    id = ID_SEP.join(arguments)

    return id


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


def generate_test_table():
    rng = np.random.default_rng()

    cols_count = 30
    columns = ['col_' + str(i) for i in np.arange(1, cols_count + 1)]
    data = rng.integers(0, 100, size=(100, cols_count))
    df = pd.DataFrame(data, columns=columns)

    return df
