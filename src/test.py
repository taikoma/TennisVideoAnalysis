import re
import sqlite3
import pandas as pd
import database
import score

def test_re():
    text="15-30"

    # m=re.search(r'(\d*)-',text)

    left=re.findall(r'([0-9a-zA-Z]*)-',text)
    right=re.findall(r'-([0-9a-zA-Z]*)',text)
    print(left[0],right[0])

    text="A-40"

    # left=re.findall(r'(\d*)-',text)
    left=re.findall(r'([0-9a-zA-Z]*)-',text)
    print(left[0])

def test_data():
    db_name="../data/nishioka-nakajima.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    df_shot = pd.read_sql("select * from shot", conn)

    print(df_shot)
    conn.close()

def test_database():
    sc=score.Score(0)
    db_name="../data/test.db"
    db=database.Database(db_name,sc)
    db.load_database_shot(db_name)


# test_re()
test_database()

    