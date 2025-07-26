import sqlite3

class TranslationHistory:
    def __init__(self):
        # === Step 1: Connect to SQLite and create table ===
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
            col1 INTEGER,
            col2 INTEGER,
            col3 INTEGER,
            col4 INTEGER
        )
        ''')
        self.conn.commit()
    
    def insert_row(self,row):
        self.row = row
        self.cursor.execute('INSERT INTO translation VALUES ( datetime("now","localtime"), ?, ?, ?, ?)', self.row)
        self.conn.commit()

# === Run ===
if __name__ == "__main__":
    history = TranslationHistory()
    history.insert_row()
    history.conn.close()