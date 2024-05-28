from io import TextIOWrapper
import sqlite3 as sql
import re
import random
from sqlite3.dbapi2 import Connection
import pandas as pd
from typing import Optional, List
from datetime import datetime

FILENAME = '../../MOCK_DATA.csv'
WRITE_SCRIPT = True
NUM_REC = 25

# connect to SQLite

def connectSQLite() -> Connection | None:
    query = ""
    liteCursor = None
    db: Optional[Connection] = None 
    try:
        query = """SELECT name FROM sqlite_schema where type in ('table', 'view') and name not like 'sqlite_%' order by 1;"""
# Create a SQL connection to our SQLite database
        db = sql.connect("./part3.db",
            detect_types=sql.PARSE_DECLTYPES |
            sql.PARSE_COLNAMES)
        liteCursor = db.cursor()
    except sql.Error as err:
        print("Failed to connect", err)

    if (query != "" and liteCursor is not None):
        print("Connected to SQLite for Part 3")
        print("List of Tables")
        liteCursor.execute(query)
        for t in liteCursor.fetchall():
            print(t)
        print("end")

    return db

def random_date(flag) -> datetime:
    start = None
    end = None
    startU = None
    endU = None
    unit = 's'
    if (flag == 0):
        start = pd.to_datetime('2015-01-01')
        end = pd.to_datetime('2024-01-31')
    if (flag == 1):
        start = pd.to_datetime('1968-01-01')
        end = pd.to_datetime('2000-01-01')
#    print(f"start time: '{start.time}'")
    if (flag == 3):
        start = pd.to_datetime('1980-01-01')
        end = pd.to_datetime('2022-01-01')
    #if (start is not None and end is not None):
    # Calculate the number of days since the epoch for start and end dates
        #epoch = pd.Timestamp("1970-01-01")
        #startU = (start - epoch).days
        #endU = (end - epoch).days
        #unit = 'D'
    if (start is not None and end is not None):
        startU = int(start.value//10**9)
        endU = int(end.value//10**9)

    random_date = random.randint(startU, endU)
#    return  pd.to_datetime(dt, format='%Y%m%d', errors='coerce')
    if (startU is not None and endU is not None):
        return pd.to_datetime(random_date, unit=unit)

def isEveryOther(time):
   return (random.randrange(1,100) % time == 0)

class create_owner:

    max: int = NUM_REC

    def __init__(self):
        self.id_list = []
        df = pd.read_csv(FILENAME)
        self.rd = df.sample(self.max)

    def create_sql(self) -> str:
        sqlInsert = "insert into owner (id,\
                                        last_name,\
                                        first_name,\
                                        middle_name,\
                                        email,\
                                        updated_at,\
                                        created_at\
                                        ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max): 
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            initials = row['first_name'][0] + row['middle_name'][0]
            lastname = row['last_name']
            initials = initials + lastname[0]
            cd:datetime = random_date(0)
            ud:datetime = random_date(0)
            if (cd.date() > ud.date()):
                t = cd; cd = ud; ud = t
            self.id_list.append(id)
            sqlInsert += "("+str(id)+", '"
            sqlInsert += row['last_name'].replace("'", "`")+"', '"
            sqlInsert += row['first_name'].replace("'", "`")+"', '"
            sqlInsert += row['middle_name'].replace("'", "`")+"', '"
            sqlInsert += row['email']+"', '" 
            sqlInsert += str(ud)+"', '"
            sqlInsert += str(cd)+"')" + lc
        #print(sqlInsert)
        return sqlInsert

    def get_id_list(self) -> List[int]:
        return self.id_list


class create_car:

    max: int = NUM_REC
    style: List[str] = ['4x4', 'convertible', '2 door', '4 door', 'hatch', 'EV']

    def __init__(self):
        self.id_list = []
        df = pd.read_csv(FILENAME)
        self.rd = df.sample(self.max)

    def create_sql(self):
        sqlInsert = "insert into car (id,\
                                      make,\
                                      model,\
                                      style,\
                                      year,\
                                      updated_at,\
                                      created_at\
                                      ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max): # in case this is also a preferred primary key
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            self.id_list.append(id)
            cstyle = random.choice(self.style)
            cd:datetime = random_date(0)
            ud:datetime = random_date(0)
            if (cd.date() > ud.date()):
                t = cd; cd = ud; ud = t
            sqlInsert += "("+str(id)+", '"
            sqlInsert += row['car_make']+"', '"
            sqlInsert += row['car_model']+"', '"
            sqlInsert += cstyle+"', '"
            sqlInsert += str(row['car_year'])+"', '" 
            sqlInsert += str(ud)+"', '"
            sqlInsert += str(cd)+"')" + lc
        #print(sqlInsert)
        return sqlInsert

    def get_id_list(self) -> List[int]:
        return self.id_list

class create_ownscar:

    max: int = NUM_REC
    plate_prefix: List[str] = ['HK','KFD','OR','JFD','DK','YY']

    def __init__(self):
        self.id_list = []
        df = pd.read_csv(FILENAME)
        self.rd = df.sample(self.max)

    def create_sql(self):
        sqlInsert = "insert into ownscar (id,\
                                        owner_id,\
                                        car_id,\
                                        colour,\
                                        vin,\
                                        plate_number,\
                                        purchased_dt,\
                                        updated_at,\
                                        created_at\
                                        ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max): # in case this is also a preferred primary key
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            self.id_list.append(id)
            cd:datetime = random_date(0)
            ud:datetime = random_date(0)
            if (cd.date() > ud.date()):
                t = cd; cd = ud; ud = t
            pn = random.choice(self.plate_prefix)+str(random.randrange(11111,99999))
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, NUM_REC))+", "
            sqlInsert += str(random.randrange(1, NUM_REC))+", '"
            sqlInsert += row['car_colour']+"', '"
            sqlInsert += row['car_vin']+"', '"
            sqlInsert += pn+"', '"
            sqlInsert += str(random_date(3).date())+"', '" # purchased date
            sqlInsert += str(ud)+"', '"
            sqlInsert += str(cd)+"')" + lc
        #print(sqlInsert)
        return sqlInsert

    def get_id_list(self):
        return self.id_list

def writeSqlScript(script: str) -> TextIOWrapper:
    sqlScriptFile = open("sqlScript.txt", 'w+')
        # Print and save lines with line numbers
    for line in script:
        sqlScriptFile.write(line)

    return sqlScriptFile 

conLite=None
sqlScriptFile=None
if WRITE_SCRIPT:
    conLite = connectSQLite()

owner = create_owner()
res = owner.create_sql()
if WRITE_SCRIPT:
    if (conLite is not None):
        cursor = conLite.cursor()
        cursor.execute("pragma foreign_keys = OFF;")
        cursor.execute("delete from owner;")
        cursor.execute("pragma auto_vaccuum = FULL;")
        #   cursor.execute("vacuum;")
        cursor.execute(res)
        conLite.commit()

        sqlScriptFile = writeSqlScript(res)

car = create_car()
res = car.create_sql()
if WRITE_SCRIPT:
    if (conLite is not None):
        cursor = conLite.cursor()
        cursor.execute("pragma foreign_keys = OFF;")
        cursor.execute("delete from car;")
        cursor.execute("pragma auto_vaccuum = FULL;")
        #   cursor.execute("vacuum;")
        cursor.execute(res)
        conLite.commit()

ownscar = create_ownscar()
res = ownscar.create_sql()
if WRITE_SCRIPT:
    if (conLite is not None):
        cursor = conLite.cursor()
        cursor.execute("pragma foreign_keys = OFF;")
        cursor.execute("delete from ownscar;")
        cursor.execute("pragma auto_vaccuum = FULL;")
        #   cursor.execute("vacuum;")
        cursor.execute(res)
        conLite.commit()

    if (conLite is not None):
        sqlScriptFile.close()
        conLite.cursor().close()
        conLite.close()
