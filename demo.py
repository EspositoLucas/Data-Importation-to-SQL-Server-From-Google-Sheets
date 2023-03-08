import pandas as pd # pip install pandas
import pypyodbc as odbc # pip install pypyodbc 
from Google import Create_Service

"""
Getting Dataset from Google Sheets
"""
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

google_sheets_id = ''

response = service.spreadsheets().values().get(
    spreadsheetId=google_sheets_id,
    majorDimension='ROWS',
    range='SHEET NAME'
).execute()

rows = response['values'][1:]


"""
Push Dataset to SQL Server (database system)
"""
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'SERVER NAME'
DATABASE_NAME = 'DATABASE_NAME'

def connection_stirng(driver_name, server_name, database_name):
    # uid=<username>;
    # pwd=<password>;
    conn_string = f"""
        DRIVER={{{driver_name}}};
        SERVER={server_name};
        DATABASE={database_name};
        Trust_Connection=yes;        
    """
    return conn_string

# connection object creation
try:    
    conn = odbc.connect(connection_stirng(DRIVER_NAME,SERVER_NAME,DATABASE_NAME))
    print('Connection created')    
except odbc.DatabaseError as e:
    print('Database Error:')
    print(str(e.value[1]))
except odbc.Error as e:
    print('Connection Error')
    print(str(e.value[1]))
else:
    cursor = conn.cursor()
    sql_insert = """
        INSERT INTO Table
        VALUES(?, ?, ?, ?,?,?) - number of columns
    """    
    try:
        cursor.executemany(sql_insert, rows)
        cursor.commit()
        print('Data import complete')
    except Exception as e:
        print(str(e.value[1]))
        cursor.rollback()
    finally:
        cursor.close()
        conn.close()