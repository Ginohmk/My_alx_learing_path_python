import psycopg2

connection = psycopg2.connect('dbname=example')

cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS table1;')

cursor.execute('''
  CREATE TABLE table1 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
''')

# Way one of inserting - using string literal (tuple)
cursor.execute('''
  INSERT INTO table1 (id , completed)
  VALUES (%s, %s);
''', (1,True))

SQL = 'INSERT INTO table1 (id , completed)  VALUES (%(id)s, %(completed)s);'
date = {
'id': 2,
 'completed': True
}

cursor.execute(SQL,date )

cursor.execute('''
  INSERT INTO table1 (id , completed)
  VALUES (%s, %s);
''', (3,False))

cursor.execute('SELECT * FROM table1;')

result = cursor.fetchall()

for row in result:
    print(row)

# To commit transactin
connection.commit()

# To close opened connection and cursor
connection.close()
cursor.close()
