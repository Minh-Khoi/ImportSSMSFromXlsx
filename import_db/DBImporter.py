import pandas as pd
import pyodbc as pydb
from typing import List
import GLOBALS

class DBImporter:
    def __init__(self,column_names:List[str],datafr : pd.DataFrame) -> None:
        self.column_names = list(map(lambda x: x.replace(" ","_") ,column_names))
        self.datafr = datafr
        pass
    
    def __createTable(self,connection: pydb.Connection):
        # Get the table schema from the DataFrame
        table_schema = self.column_names

        # Create the SQL statement to create the table
        create_table_sql = """IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{}'
                                and xtype='U')
                            CREATE TABLE {} (""".format(GLOBALS.DB_FILE_NAME,GLOBALS.DB_FILE_NAME)
        for column, data_type in zip(table_schema, self.datafr.dtypes):
            create_table_sql += f'{column} nvarchar(250), '
        create_table_sql = create_table_sql[:-2] + ')'

        # Execute the SQL statement
        try:
            cursor = connection.cursor()
            cursor.execute(create_table_sql)
            connection.commit()
            print('Table created or already exists')
        except pydb.Error as e:
            print('Error creating table:', e)
            
    def writeDB(self, connection: pydb.Connection):
        self.__createTable(connection=connection)
        # Insert the DataFrame data into the table
        cursor = connection.cursor()
        try:
            for index, rowS in self.datafr.fillna(value=" ").loc[1:].iterrows():
                row = self.__formatDatasOfRow(row=rowS)
                insertSQL = """INSERT INTO {} (""".format(GLOBALS.DB_FILE_NAME) \
                                    + ", ".join(self.column_names) \
                                +""") values("""\
                                    + ", ".join(row)\
                                +""")"""
                cursor.execute(insertSQL)
            
            connection.commit()
            print('Data inserted into SQL Server table')
        except pydb.Error as e:
            print('Error inserting data:', e)
            
            
    def __formatDatasOfRow(self, row : pd.Series) -> list:
        listForRow = row.to_list()
        listForRow = list(map(lambda d : "N'{}'".format(d),listForRow))
        return listForRow