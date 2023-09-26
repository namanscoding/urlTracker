from datetime import datetime
from queries import *
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(dbname=os.getenv(
    "dbname"), user=os.getenv("user"), password=os.getenv("password"))


# ---------db Handlers----------------------


# CREATE
def create_urls_table_iff():
    cursor = connection.cursor()
    try:
        cursor.execute(CREATE_URLS_TABLE)
        connection.commit()
    except:
        connection.rollback()
        print("Rolled Back")
    cursor.close()


# CREATE
def insert_url(url, hash, content):
    print("-"*60)
    cursor = connection.cursor()
    try:
        print(f'Inserting URL : {url}')
        cursor.execute(INSERT_URL, (str(url), str(hash), str(content) ))
        connection.commit()
    except:
        connection.rollback()
        print("Rolled Back")
    cursor.close()
    print("-"*60)


# READ
def fetch_all_db():   
    cursor = connection.cursor()
    try:
        cursor.execute(FETCH_ALL)
        data = cursor.fetchall()
        connection.commit()
        return data
    except:
        connection.rollback()
        print("Rolled Back")
    cursor.close()
    


# UPDATE
def update_row(url, hash,prevcontent):
    #revhash=%s,prevcontent=%s, timestamp = %s WHERE  url=%s
    print("-"*60)
    cursor = connection.cursor()
    try:
        print(f'Updating URL : {url}')
        cursor.execute(UPDATE_HASH_TIME, (str(hash),str(prevcontent),
                       str(datetime.now()), str(url), ))
        connection.commit()
    except:
        connection.rollback()
        print("Rolled Back")
    cursor.close()
    print("-"*60)


# DELETE
def delete_from_db(url):
    print("-"*60)
    cursor = connection.cursor()
    try:
        print(f'Deleting URL : {url}')
        cursor.execute(DELETE_URL, (str(url),))
        connection.commit()
    except:
        connection.rollback()
        print(cursor.rowcount)
        print("Rolled Back")
    cursor.close()
    print("-"*60)
