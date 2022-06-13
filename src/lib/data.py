import os

import pandas as pd


def read_data(name: str, *, folder: str) -> pd.DataFrame:
    """
    Reads data from a csv file.
    """

    return pd.read_csv(os.path.join(os.getcwd(), folder, name), header=0)
