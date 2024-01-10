from flask import Flask,render_template,request,jsonify,make_response
from dao.UserDao import save,find,createUserTable
from models.User import User

from services.UserService import *
from loansapp import loansapp
from tokenapp import tokenapp
from flask_jwt_extended import JWTManager
app = Flask(__name__)
app.register_blueprint(loansapp)
app.register_blueprint(tokenapp)
app.config["JWT_SECRET_KEY"] = "super-secret" 
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_PORT']=3306
app.config['MYSQL_DB']='flaskdb'

jwt=JWTManager(app);
@app.route("/")

def home() :
   
    return render_template('index.html')
@app.route("/signin",methods=["GET","POST"])
def signin():
    if request.method == "POST" :
       #print(request.form['username'])
       return render_template('userhome.html')
    return render_template('login.html')
@app.route('/login',methods=["POST"])
def login() :

    if request.method=='POST':

      username=request.args.get('username')
      password=request.args.get('password');
      if isValidLigin(username,password) :
       return "Valid User"
      else:
       return "Invalid Credentials"
   
@app.route('/signup',methods=["GET","POST"])
def signup() :
    if request.method == "POST":
       user:User = User(request.form['fullname'],request.form['email'],request.form['username'],request.form['password']);
       print(user)
       return "User Created Successfully"+user.fullname
    return render_template('signup.html')
@app.route('/register',methods=["POST"])
def registerUser():
   userRequest = request.get_json();
   user:User = User(userRequest["fullname"],userRequest["email"],userRequest["username"],userRequest["password"]);
   

   if(createUser(user)):
       response = make_response('User creation sucessfull',201)
       return response;
   else:
      response =make_response('User Not Created ',501)
   return  response;
   
@app.route('/apply')
def apply() :
    return render_template('apply.html')


@app.errorhandler(Exception)
def handle_exception(e):
    print(e)

    return str(e)


if __name__ == '__main__':
    createUserTable();
    app.run(debug=True)