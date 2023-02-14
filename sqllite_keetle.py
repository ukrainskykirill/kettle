import sqlite3

connection = sqlite3.connect('kettle.db', check_same_thread=False)

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Kettle_table (
    attemp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    water REAL NOT NULL,
    temp INTEGER NOT NULL,
    state TEXT NOT NULL,
    date datetime);
''')

insert_with_param = '''
    INSERT INTO Kettle_table
    (water, temp, state, date)
    VALUES (?, ?, ?, ?);
'''

connection.commit()
