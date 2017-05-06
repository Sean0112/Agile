from flask import Flask, render_template, request, flash
from wtforms import Form, BooleanField, SelectField, TextField, validators, PasswordField
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

cur.execute("SELECT * FROM information_schema.tables WHERE table_name ='{}'".format("Alumni"))
if cur.rowcount == 0:
    cur.execute("CREATE TABLE Alumni(Id SERIAL PRIMARY KEY, Name VARCHAR(20), Email VARCHAR(50), Password VARCHAR(20), Degree VARCHAR(20), Year INT)")
# cur.execute("INSERT INTO Alumni (Name, Email, Degree, Year) VALUES('Edward', 'emarc@gmail.com','Computer Science', 2017)")
# cur.execute("INSERT INTO Alumni (Name, Email, Degree, Year) VALUES('Christopher', 'chris@gmail.com', 'Computer Science', 2018)")
# cur.execute("INSERT INTO Alumni (Name, Email, Degree, Year) VALUES('Jeff', 'jeffgrammer492@myci.csuci.edu', 'Computer Science', 2018)")
# cur.execute("INSERT INTO Alumni (Name, Email, Degree, Year) VALUES('Kelsey','its_k_betch@gmail.com', 'Robotics', 2020)")
# cur.execute("INSERT INTO Alumni (Name, Email, Degree, Year) VALUES('Andrew', 'adawg@gmail.com','Business', 2019)")

def updateDatabase(name, email, password, graduation_year, major):
    cur.execute("INSERT INTO Alumni (Name, Email, Password, Degree, Year) VALUES (%s, %s, %s, %s, %s)",(name, email, password, major, graduation_year))
    conn.commit()
    cur.execute("SELECT name, degree, year FROM {}".format("Alumni"))
    data_html = ""
    rows = cur.fetchall()
    for row in rows:
        data_html += "<tr>"
        print(row)
    conn.close()

app = Flask(__name__)
app.secret_key = 'some_secret'

class InputForm(Form):
    select_field = SelectField(choices=[('Math','Mathematics'),('CS','Computer Science'),('Biz','Business'),('Anthro','Anthropology'),('Art','Art'),('Bio','Biology'),('Spanish','Spanish'),('Psych','Psychology'),('Nursing','Nursing')], validators=[validators.InputRequired()])
    boolean_field = BooleanField()
    name_field = TextField([validators.InputRequired()])
    email_field = TextField([validators.InputRequired()])
    password_field = PasswordField([validators.InputRequired()])
    grad_field = TextField([validators.InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    result_str = None
    form = InputForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name_field.data
        email = form.email_field.data
        password = form.password_field.data
        graduation_year = form.grad_field.data
        major = form.select_field.data
        boolean_val = form.boolean_field.data

        if boolean_val != True:
           print("Got to Flash")
           flash ("You must check the box to be added.")
        else:
            updateDatabase(name, email, password, graduation_year, major)
            result_str = "Congratulations, {} you've been added to the system".format(name)

    return render_template("index.html", template_form=form, result=result_str)

if __name__ == '__main__':
    app.run(port=3560)
