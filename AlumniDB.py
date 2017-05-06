import psycopg2

def myurlparse(url):
    start = url.index('@')
    end = url.index('.com:')
    Host = url[start+1:end+4]
    Port = url[end+5:end+9]
    Database = url[end+10:]
    start =url.index('://')+3
    end = url[start:].index(':')+start
    User = url[start:end]
    Password = url[end+1:url.index('@')]
    return Database, Host, Port, User, Password

url = 'postgres://bguglhxikjlabk:92dfba8e4d63f081e166cf3d0ceb07b12fe490091dda15da227e20a4af76057b@ec2-54-163-252-55.compute-1.amazonaws.com:5432/d1h440up5d3stn'

try:
    dbname, host, port, user, password = myurlparse(url)
    conn = psycopg2.connect(dbname=dbname,
                            host = host,
                            port = port,
                            user = user,
                            password = password)
except:
    print("I am unable to connect to the database")

cur = conn.cursor()
cur.execute('SELECT version()')
ver = cur.fetchone()
print (ver)

cur.execute("DROP TABLE Alumni")

cur.execute("CREATE TABLE Alumni(Id SERIAL PRIMARY KEY, Name VARCHAR(20), Degree VARCHAR(20), Year INT)")
cur.execute("INSERT INTO Alumni (Name, Degree, Year) VALUES('Edward', 'Computer Science', 2017)")
cur.execute("INSERT INTO Alumni (Name, Degree, Year) VALUES('Christopher', 'Computer Science', 2018)")
cur.execute("INSERT INTO Alumni (Name, Degree, Year) VALUES('Sean', 'Mathematics', 2017)")
cur.execute("INSERT INTO Alumni (Name, Degree, Year) VALUES('Jeff', 'Computer Science', 2018)")
cur.execute("INSERT INTO Alumni (Name, Degree, Year) VALUES('Kelsey', 'Robotics', 2020)")
cur.execute("INSERT INTO Alumni (Name, Degree, Year) VALUES('Andrew', 'Business', 2019)")

conn.commit()

cur.execute("SELECT * FROM Alumni")

data_html = ""
rows = cur.fetchall()
for row in rows:
    data_html += "<tr>"
    print (row)

conn.close()

