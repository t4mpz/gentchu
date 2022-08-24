# from database.db_json_core import JSONDatabase
from database.objects import *
from database.psql_db import *

dc = Distros()

print(dc.get_distro_url("debian"))

