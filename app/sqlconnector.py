# from flask import Flask
# from flask import render_template, request, redirect, url_for, flash
# # from flask_mysql_connector import MySQL
# from flask_mysqldb import MySQL


# app = Flask(__name__)
# # app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DATABASE'] = 'arMapsDB'
# mysql = MySQL(app)


# cur = mysql.connection.cursor()
# cur.execute("SELECT * FROM users")
# fetchdata = cur.fetchall()
# print(fetchdata)
# cur.close()

# # @app.route('/')
# # def home():
# #     cur = mysql.connection.cursor()
# #     cur.execute("SELECT * FROM users")
# #     fetchdata = cur.fetchall()
# #     cur.close()
# #     """Render website's home page."""
# #     return render_template('index.html', data = fetchdata)


# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)


@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)

if __name__ == '__main__':
    app.run(debug=True)