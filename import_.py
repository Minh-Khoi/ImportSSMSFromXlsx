import pyodbc

from excelmodels.XlsxDatas import XlsxDatas
from import_db.DBImporter import DBImporter
import accessDBConfig.config as dbconfig
import GLOBALS as global_s

# Create a connection string using the ODBC driver and connection details
connection_string = """DRIVER={};SERVER={};DATABASE={};UID={};PWD={}""".format(
                        "{SQL Server}",
                        dbconfig.server,dbconfig.database,dbconfig.name,dbconfig.password
                    )

excel = XlsxDatas()
excel.readDatas()

# Connect to the SQL Server database
connection : pyodbc.Connection
try:
    connection = pyodbc.connect(connection_string)
    print('Connected to SQL Server database')
    db_importer = DBImporter(excel.column_names,excel.datas)
    db_importer.writeDB(connection=connection)
except pyodbc.Error as e:
    print('Error connecting to SQL Server:', e)


connection.close()
print('Database connection closed')