from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import json

app = Flask(__name__)
def db_init():
    mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1",
    auth_plugin='mysql_native_password'
     )
    cursor = mydb.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS PersonalInfo")
    cursor.close()

    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="PersonalInfo",
        auth_plugin='mysql_native_password'
    )
    cursor = mydb.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Info 
            (
                Name VARCHAR(255), 
                AGE VARCHAR(255),
                Country VARCHAR(255), 
                Company VARCHAR(255), 
                Designation VARCHAR(255)
            )"""
    )
    cursor.close()
    return 'Database Initialized' 
 
@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route("/getInfo")
def get_info():
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1",
    database="PersonalInfo"
  )
  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM Info")

  row_headers=[x[0] for x in cursor.description] #this will extract row headers

  results = cursor.fetchall()
  print(results)
  json_data=[]
  for result in results:
    json_data.append(dict(zip(row_headers,result)))

  cursor.close()
  return json.dumps(json_data)


@app.route('/', methods=['POST'])
def my_form_post():
    name = request.form['name'].title()
    age = request.form['age']
    country = request.form['country'].title()
    company = request.form['company'].title()
    designation = request.form['designation'].title()
    print(db_insert(name,age,country,company,designation))
    return redirect(url_for('get_info'))
    
def db_insert(name,age,country,company,designation):
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1",
    database="PersonalInfo",
    auth_plugin='mysql_native_password'
  )
  cursor = mydb.cursor()
  val = (name,age,country,company,designation)
  cursor.execute("Insert into Info values(%s,%s,%s,%s,%s)",val)
  mydb.commit()
  cursor.close()
  return 'insert database rows'


if __name__=="__main__":
    print(db_init())
    app.run(host ='0.0.0.0')