from io import TextIOWrapper
import sqlite3 as sql
import bcrypt
import re
import json
import random
from sqlite3.dbapi2 import Connection
import pandas as pd
# import const
# import services
# import locations
from typing import Optional, List
from datetime import datetime

global fileName, WRITE_SCRIPT
ctype:List = ["freelancer","commission","hourly","salaried","none"]
   
fileName = '../../MOCK_DATA.csv'
WRITE_SCRIPT = True

# connect to SQLite

def connectSQLite() -> Connection | None:
    query = ""
    liteCursor = None
    db: Optional[Connection] = None 
    try:
        query = """SELECT name FROM sqlite_schema where type in ('table', 'view') and name not like 'sqlite_%' order by 1;"""
# Create a SQL connection to our SQLite database
        db = sql.connect("./part1.db",
            detect_types=sql.PARSE_DECLTYPES |
            sql.PARSE_COLNAMES)
        liteCursor = db.cursor()
    except sql.Error as err:
        print("Failed to connect", err)

    if (query != "" and liteCursor is not None):
        print("Connected to SQLite for Part 1")
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
    if (flag == 0):
      start = pd.to_datetime('2015-01-01')
      end = pd.to_datetime('2024-01-31')
    if (flag == 1):
      start = pd.to_datetime('1968-01-01')
      end = pd.to_datetime('2002-01-31')
#    print(f"start time: '{start.time}'")
    if (start is not None and end is not None):
        startU = start.value//10**9
        endU = end.value//10**9
#    dt = random.randint(startU, endU)
#    return  pd.to_datetime(dt, format='%Y%m%d', errors='coerce')
    if (startU is not None and endU is not None):
        return pd.to_datetime(random.randint(startU, endU), unit='s')

def isEveryOther(time):
   return (random.randrange(1,100) % time == 0)

def create_contract():
    hours = random.randrange(20,80)
    rate =  random.randrange(25,150) * 100
    numc =  random.randrange(1,15)
    comm =  random.randrange(1,15)
    over =  random.randrange(1000,5505)
    salary =  random.randrange(40000,150000) * 100

    c = random.choice(ctype)
    match(c):
        case "freelancer":
            contract = {"ctype": c, "hours": hours, "rate": rate}
        case "hourly":
            contract = {"ctype": c, "hours": hours, "rate": rate, "overhead":over}
        case "commission":
            contract = {"ctype": c, "commission": comm, "num_contracts":numc}
        case "salaried":
            contract = {"ctype": c, "salary": salary, "hours": hours}
        case "none":
            contract = {"ctype": c}

    return json.dumps(contract)

class create_employee:

    max: int = 20

    def __init__(self):
        self.uuid_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):
        sqlInsert = "insert into employee (id,\
                                           emp_number,\
                                           username,\
                                           last_name,\
                                           first_name,\
                                           middle_name,\
                                           salary,\
                                           email,\
                                           hashed_password,\
                                           contract_type,\
                                           updated_at,\
                                           created_at\
                                           ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        password = b'password'
        salt = bcrypt.gensalt()
        hpass = bcrypt.hashpw(password, salt)
        for id in range(1, self.max): # in case this is also a preferred primary key
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            uuid = row['UUID']
            cd:datetime = random_date(0)
            ud:datetime = random_date(0)
            if (cd.date() > ud.date()):
                t = cd; cd = ud; ud = t
        #{'ctype': 'freelancer', 'rate': 3000, 'hours':5300}
            initials = row['first_name'][0] + row['middle_name'][0]
            lastname = row['last_name']
            username = initials + lastname
            initials = initials + lastname[0]
            emp_number = initials + str(random.randrange(1928, 4394)) 
            cjson = create_contract() 
            self.uuid_list.append(uuid)
            sqlInsert += "('"+str(uuid)+"', '"
            sqlInsert += emp_number +"', '"
            sqlInsert += username +"', '"
            sqlInsert += row['last_name'].replace("'", "`")+"', '"
            sqlInsert += row['first_name'].replace("'", "`")+"', '"
            sqlInsert += row['middle_name'].replace("'", "`")+"', '"
            sqlInsert += str(random.randrange(40000,140000)*100)+"', '"
            sqlInsert += row['email']+"', '" 
            sqlInsert += str(hpass).replace("'", "`") +"', '"
            sqlInsert += cjson+"', '"
            #sqlInsert += str('`{"ctype": ')+contract+str(', "rate": ')+str(rate)+str(', "hours": ')+str(hours)+"}`"+"', '"
            sqlInsert += str(random_date(0))+"', '"
            sqlInsert += str(random_date(0))+"')" + lc
        print(sqlInsert)
        return sqlInsert

    def get_id_list(self):
        return self.uuid_list


def writeSqlScript(script: str) -> TextIOWrapper:
    sqlScriptFile = open("sqlScript.txt", 'w+')
    for line in script:
        sqlScriptFile.write(line)

    return sqlScriptFile 

conLite=None
sqlScriptFile=None
if WRITE_SCRIPT:
    conLite = connectSQLite()

employee = create_employee()
res = employee.create_sql()
if WRITE_SCRIPT:
    if (conLite is not None):
        cursor = conLite.cursor()
        cursor.execute("pragma foreign_keys = OFF;")
        cursor.execute("delete from employee;")
        cursor.execute("pragma auto_vaccuum = FULL;")
        #   cursor.execute("vacuum;")
        cursor.execute(res)
        conLite.commit()

        sqlScriptFile = writeSqlScript(res)

    if (conLite is not None):
        sqlScriptFile.close()
        conLite.cursor().close()
        conLite.close()
