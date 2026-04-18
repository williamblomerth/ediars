import sys
import os
import numpy as np
wd = sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.csv_ingestor import adapt_to_sql
from src.csv_ingestor import main


def test_answer():
    sql_cmd = main(os.path.append(wd, 'data/favorite_pokemon.csv'))
    assert  sql_cmd[0] == "CREATE TABLE favorite_pokemon(Name, Primary_Type, Secondary_Type, Region, Favorite_By);"

# test for proper syntax and valid commands


# test for valid query


# test for not allowed commands (delete everything, etc)
