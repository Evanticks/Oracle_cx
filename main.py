import cx_Oracle

connection=cx_Oracle.connect(
	user='antonio',
	password='antonio',
	dsn='192.168.122.20:1521/ORCLCDB',
	encoding='UTF-8'
)
print(connection.version)

cursor = connection.cursor()

cursor.execute("select * from tesoro")
res = cursor.fetchall()

for linea in res:
    linea = list(linea)
    print(linea[3])