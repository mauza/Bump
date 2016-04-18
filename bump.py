from flask import Flask, render_template, request, json, session, redirect
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.debug = True

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'mauza'
app.config['MYSQL_DATABASE_PASSWORD'] = 'caster11'
app.config['MYSQL_DATABASE_DB'] = 'bump'
app.config['MYSQL_DATABASE_HOST'] = 'work.mauza.net'
mysql.init_app(app)

app.secret_key = "this is a secrect, that is why you will never know it"

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html', errorDisplay="display: none;", sDisplay = "display: none;")

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html', errorDisplay="display: none;")

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return redirect('/showSignIn')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            try:
              conn = mysql.connect()
              cursor = conn.cursor()
              _hashed_password = generate_password_hash(_password)
              cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
              data = cursor.fetchall()

              if len(data) is 0:
                conn.commit()
                return render_template('signin.html', errorDisplay="display: none;", sDisplay = "")
              else:
                return render_template('signup.html',error = str(data[0])[3:-3], errorDisplay = "")
                #return json.dumps({'error':str(data[0])})
            except:
              return render_template('signup.html',error = 'SQL ERROR', errorDisplay = "")
            finally:
              cursor.close()
              conn.close()
        else:
            return render_template('signup.html',error = 'Enter the required fields', errorDisplay = "")

    except Exception as e:
        return json.dumps({'error':str(e)})
        

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
 
 
 
        # connect to mysql
 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
 
 
 
 
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('signin.html',error = 'Wrong Email address or Password.', errorDisplay = "", sDisplay = "display: none;")
                #return json.dumps({'html':'<span>Wrong Email address or Password.</span>'})
        else:
            return render_template('signin.html',error = 'Wrong Email address or Password.', errorDisplay = "", sDisplay = "display: none;")
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()



#for Cloud 9
app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))

if __name__== "__main__":
    app.run()
