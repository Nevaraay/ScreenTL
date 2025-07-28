import sqlite3
from datetime import datetime

class TranslationHistory:
    def __init__(self):
        # Connect to SQLite and create table
        self.conn = sqlite3.connect('my_database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS translation (
            col1 TEXT,
            col2 TEXT,
            col3 TEXT,
            col4 TEXT,
            col5 TEXT
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage (
            year TEXT,
            month TEXT,
            day TEXT,
            col1 INTEGER,
            col2 INTEGER,
            col3 INTEGER
        )
        ''')
        self.conn.commit()
    
    def insert_row(self,row):
        self.cursor.execute('INSERT INTO translation VALUES ( datetime("now","localtime"), ?, ?, ?, ?)', row)
        self.conn.commit()
        
    def insert_bar(self, val_1=0,val_2=0,val_3=0):
        today = datetime.now()
        day = today.day
        month = today.month
        year = today.year

        # Check if a row with today's month already exists
        self.cursor.execute("SELECT COUNT(*) FROM usage WHERE (month,year) = (?,?)", (month,year))
        count = self.cursor.fetchone()[0]

        if count == 0:
            self.cursor.execute("INSERT INTO usage VALUES (?, ?, ?, ?, ?, ?)", (year,month,day, val_1, val_2, val_3)) 
            self.conn.commit()
            print("Inserted row this for month.")
        else:
            # Check if row for today already exists
            self.cursor.execute("SELECT col1,col2,col3 FROM usage WHERE (day, month, year) = (?, ?, ?)", (day, month, year))
            recent = self.cursor.fetchone()
            if recent:
                # When a row for this day & month already exists
                col_1, col_2, col_3 = recent
                self.cursor.execute('''
                    UPDATE usage
                    SET col1 = ?, col2 = ?, col3 = ?
                    WHERE day = ? AND month = ?
                ''', (col_1 + val_1, col_2 + val_2, col_3 + val_3, day, month))
                
                self.conn.commit()
            else:
                self.cursor.execute("INSERT INTO usage VALUES (?, ?, ?, ?, ?, ?)", (year,month,day, val_1, val_2, val_3)) 
                self.conn.commit()


# === Run ===
if __name__ == "__main__":
    history = TranslationHistory()
    history.insert_bar()
    history.conn.close()