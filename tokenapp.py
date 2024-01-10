from flask import Blueprint,request,jsonify
from services.AuthService import *

tokenapp = Blueprint('tokenapp',__name__);

@tokenapp.route("/token",methods=["POST"])
def craeteToekn():
     user = request.get_json();
     access_token = getToken(user['username'],user['password'])
     return jsonify({"access_token":access_token})