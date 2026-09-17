# backend/app/data_pipeline/load.py

from app.services import dbl
import pandas as pd


# pseudocode
def load_data_to_db(data: pd.DataFrame):

    db = dbl.connect()
    dbl.addToToday(data)
    db.disconnect()


