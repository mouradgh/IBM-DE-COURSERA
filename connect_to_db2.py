# This code will help you connect to IBM's cloud database db2, and execute basic queries

import ibm_db

# Replace the placeholder values with your actual Db2 hostname, username, and password:
dsn_hostname = "3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
dsn_uid = "zzc19682"
dsn_pwd = "mw9yI35cCedp5pd0"

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "bludb"
dsn_port = "31498"
dsn_protocol = "TCPIP"
dsn_security = "SSL"

# Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,dsn_security)

# Create the database connection

try:
    conn = ibm_db.connect(dsn, "", "")
    print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

except:
    print ("Unable to connect: ", ibm_db.conn_errormsg())


# Retrieve Metadata for the Database Server
server = ibm_db.server_info(conn)

print ("DBMS_NAME: ", server.DBMS_NAME)
print ("DBMS_VER:  ", server.DBMS_VER)
print ("DB_NAME:   ", server.DB_NAME)


# Retrieve Metadata for the Database Client / Driver
client = ibm_db.client_info(conn)

print ("DRIVER_NAME:          ", client.DRIVER_NAME)
print ("DRIVER_VER:           ", client.DRIVER_VER)
print ("DATA_SOURCE_NAME:     ", client.DATA_SOURCE_NAME)
print ("DRIVER_ODBC_VER:      ", client.DRIVER_ODBC_VER)
print ("ODBC_VER:             ", client.ODBC_VER)
print ("ODBC_SQL_CONFORMANCE: ", client.ODBC_SQL_CONFORMANCE)
print ("APPL_CODEPAGE:        ", client.APPL_CODEPAGE)
print ("CONN_CODEPAGE:        ", client.CONN_CODEPAGE)


# Construct the Create Table DDL statement
createQuery = "create table INSTRUCTOR(ID INTEGER PRIMARY KEY NOT NULL, FNAME VARCHAR(20), LNAME VARCHAR(20), CITY VARCHAR(20), CCODE CHAR(2))"

# Execute the statement
createStmt = ibm_db.exec_immediate(conn,createQuery)

# Insert data into the table
insertQuery = "insert into INSTRUCTOR values (1, 'Rad', 'Mou', 'Lille', 'FR'), (2, 'El', 'Gh', 'Kenitra', 'MA')"
insertStmt = ibm_db.exec_immediate(conn, insertQuery)

# Query data in the table
selectQuery = "select * from INSTRUCTOR"
selectStmt = ibm_db.exec_immediate(conn, selectQuery)

# This can also be done using Pandas
# import pandas
# import ibm_db_dbi
# pconn = ibm_db_dbi.Connection(conn)
# pdf = pandas.read_sql(selectQuery, pconn)
# pdf.shape

# Fetch the Dictionary (for the first row only)
ibm_db.fetch_both(selectStmt)

# Fetch the rest of the rows and print the ID and FNAME for those rows
while ibm_db.fetch_row(selectStmt) != False:
    print (" ID:",  ibm_db.result(selectStmt, 0), " FNAME:",  ibm_db.result(selectStmt, "FNAME"))

# Update the data in the table
updateQuery = "update INSTRUCTOR set CITY='Paris' where FNAME='Rad'"
updateStmt = ibm_db.exec_immediate(conn, updateQuery)

# Close the connexion
ibm_db.close(conn)

