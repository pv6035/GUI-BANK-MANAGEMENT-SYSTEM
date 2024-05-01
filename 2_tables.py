import mysql.connector as sql
from mysql.connector import Error

conn = sql.connect(host="localhost", user="root", passwd="root@123", database="the_royal_bank")
mycursor = conn.cursor()

SQL_cmd1 = "CREATE TABLE user_table(Username varchar(25) primary key,\
Password int not null)" #SQL query to create table 'user_table'.

SQL_cmd2 = "CREATE TABLE customer_details(Account_Number int primary key,\
Account_Name varchar(25),\
City varchar(10),\
Phone_no bigint(15),\
DOB date,\
Gender char(2),\
Email varchar(30),\
Account_Type char(2),\
Initial_Amount int)" #SQL query to create table 'customer_details'.

SQL_cmd3 = "CREATE TABLE transactions(Transaction_ID int AUTO_INCREMENT PRIMARY KEY,\
Account_Number int, Date date,\
Withdrawal_Amount bigint(20), Amount_Deposited bigint(20))" #SQL query to create table 'transactions'.

SQL_cmd4 = "CREATE TABLE change_table(Change_ID int AUTO_INCREMENT PRIMARY KEY,\
Account_Number int, Date date, Old varchar(35), New varchar(35))" #SQL query to create table 'change_table'.

try:
    mycursor.execute(SQL_cmd1) #Executing the SQL query 'SQL_cmd1'.
    print("Query OK, table, 'user_table' added.")
except sql.Error as err:
    print(err)
    
try:
    mycursor.execute(SQL_cmd2) #Executing the SQL query 'SQL_cmd2'.
    print("Query OK, table, 'customer_details' added.")
except sql.Error as err:
    print(err)
    
try:
    mycursor.execute(SQL_cmd3)
    print("Query OK, table, 'transactions' added.") #Executing the SQL query 'SQL_cmd3'.
except sql.Error as err:
    print(err)

try:
    mycursor.execute(SQL_cmd4) #Executing the SQL query 'SQL_cmd4'.
    print("Query OK, table, 'change_table' added.")
except sql.Error as err:
    print(err)
