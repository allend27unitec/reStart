from io import TextIOWrapper
import sqlite3 as sql
import bcrypt
import re
from uuid import UUID, uuid4()
import csv
import random
from sqlite3.dbapi2 import Connection
import pandas as pd
# import const
# import services
# import locations
from typing import Optional

global fileName, WRITE_SCRIPT
   
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

def random_date(flag):
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
                                           contract_id,\
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
            initials = row['first_name'][0] + row['middle_name'][0]
            lastname = row['last_name']
            username = initials + lastname
            initials = initials + lastname[0]
            emp_number = initials + str(random.randrange(1928, 4394)) 
            self.uuid_list.append(uuid)
            sqlInsert += "('"+str(uuid)+"', '"
            sqlInsert += emp_number +"', '"
            sqlInsert += username +"', '"
            sqlInsert += row['last_name'].replace("'", "`")+"', '"
            sqlInsert += row['first_name'].replace("'", "`")+"', '"
            sqlInsert += row['middle_name'].replace("'", "`")+"', "
            sqlInsert += str(random.randrange(4000000,14000000))+", '"
            sqlInsert += row['email']+"', '" 
            sqlInsert += str(hpass).replace("'", "`") +"', '"
            sqlInsert += str(random.randrange(1, 5))+", "
            sqlInsert += str(random_date(0))+"')" + lc
        print(sqlInsert)
        return sqlInsert

    def get_id_list(self):
        return self.uuid_list


class create_contract:

    max: int = 5

    def __init__(self):
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)
    def create_sql(self):
        c_list = ['Freelance', 'Hourly', 'Salaried', 'Commission', 'None']
        sqlInsert = "insert into contract (id,\
                                           name,\
                                           description\
                                           ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            self.id_list.append(id)
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, const.CC_MAX))+", "
            sqlInsert += str(random.randrange(1, const.LOC_MAX))+", '"
            sqlInsert += str(random_date(0))+"', "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", '"
            sqlInsert += str(random_date(1))+"', '"
            sqlInsert += row['last_name'].replace("'", "`")+"', '"
            sqlInsert += row['first_name'].replace("'", "`")+"', '"
            sqlInsert += random.choice(middleName_list)+"', '"
            sqlInsert += row['phone'][-4:]+"', '"
            sqlInsert += random.choice(dc_list)+"', '"
            sqlInsert += row['street_addr']+"', '"
            sqlInsert += row['city']+"', "
            sqlInsert += row['phone']+", " 
            sqlInsert += row['phone'].replace('-','')+")" +lc
        print(sqlInsert)
        return sqlInsert

    def get_id_list(self):
        return self.id_list

class create_personnel:

    def __init__(self):
        self.max = const.PER_MAX 
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):
        sqlInsert = "insert into ppt_personnel (nominal_ptr_id,\
                                                 dateStart,\
                                                 dateModified,\
                                                 contractor_id,\
                                                 services_id\
                                                 ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", '"
            sqlInsert += str(random_date(1))+"', '"
            sqlInsert += str(random_date(1))+"', "
            sqlInsert += str(random.randrange(1, const.CON_MAX))+", "
            sqlInsert += str(random.randrange(1, 40))+")"+lc
        print(sqlInsert)
        return sqlInsert

# open file for reading
def openDataFile():
    global filename
    companyName = []
    abn = []

    with open(fileName, "r", encoding='latin-1') as dFile:

        ndx = random.randrange(1, 1000)
    # read file as csv file
        csvReader = csv.reader(dFile)
        row1 = next(csvReader)
        print(row1)
#       for every row, print the row
        for row in csvReader:
            companyName.append(row[6])
            abn.append(row[5])
        dFile.close()
        print("company at ndx "+str(ndx)+" "+companyName[ndx]+" with abn "+abn[ndx]) 

def writeSqlScript(script: str) -> TextIOWrapper:
    sqlScriptFile = open("sqlScript.txt", 'w+')
        # Print and save lines with line numbers
    for line in script:
        sqlScriptFile.write(line)

    return sqlScriptFile 

if WRITE_SCRIPT:
    conLite = connectSQLite()

    employee = create_employee()
    res = employee.create_sql()
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
