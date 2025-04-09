import sys
sys.path.append('..')
from utils.database import *

__db_user = 'postgres'
__db_password = '123'
__db_database = 'contents'


db = PSQLDatabase(
    user=__db_user,
    password=__db_password,
    database=__db_database
)

db.clear_all()
