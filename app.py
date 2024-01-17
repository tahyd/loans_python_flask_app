from flask import Flask,render_template,request,jsonify,make_response
from dao.UserDao import save,find,createUserTable
from models.User import User
from loansapp import isEligibleForLoan
from services.UserService import *
from loansapp import loansapp
from tokenapp import tokenapp
from flask_jwt_extended import JWTManager
import json
import pickle
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
       print(request.form['username'])
       username = request.form['username']
       password = request.form['password']
       if isValidLigin(username,password) :
        resp  = make_response(render_template('userhome.html',username=username))
        resp.set_cookie('username',username);
        #return render_template('userhome.html',username='krishna')
        return resp
       else :
        return "Invalid Credentils"
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
       if save(user) :
        return "Hi "+ user.fullname+" your data is scuccessfully stored"
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
   
@app.route('/apply',methods=["GET","POST"])
def apply() :
   
    username = request.cookies.get('username');
   

    if request.method=="POST":
       dependents = int(request.form['dependents'])
       print(dependents)
       education  =int(request.form['education'])
       print(education)
       credit_history = int(request.form['chistory'])
       print(credit_history)
       propertyArea = int(request.form['p_area'])
       print(propertyArea)
       income = float(request.form['income'])
       print(income)
       amount = float(request.form['amount'])
       print(amount)
       
       
       with open('scaler.pkl','rb') as f1:
         
         scalar_model = pickle.load(f1);
       
         
         data=scalar_model.transform([[income,amount]])
         p1=data[0,0];
         p2=data[0,1];
         
       with open('logistic_loan.pkl','rb') as f:
          
       
        loans_model = pickle.load(f)
        pridiction_result =loans_model.predict([[1,1,dependents,education,p1,p2,credit_history,propertyArea]])  
        print(str(pridiction_result[0]))
        if str(pridiction_result[0]) == "1":
           return render_template('apply.html',message='You are eligibile for loan',username=username)
        else : 
            return render_template('apply.html',message='You are  not eligibile for loan',username=username)
      
    return render_template('apply.html',username=username)

@app.route('/logout')
def logout() :
   return render_template('index.html',logout_message='You are logged out successfully')

@app.errorhandler(Exception)
def handle_exception(e):
    print(e)

    return str(e)


if __name__ == '__main__':
    #createUserTable();
    app.run(debug=True)