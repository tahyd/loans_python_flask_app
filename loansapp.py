from flask import Blueprint,request
import pickle
from sklearn.preprocessing import StandardScaler
from flask_jwt_extended import jwt_required

loansapp = Blueprint("loansapp",__name__);

@loansapp.route("/check-eligibility",methods =["POST"])
#@jwt_required(locations=["headers"])
def checkLoanEligibility() :

    loan_application = request.get_json();
    print(loan_application)
    return isEligibleForLoan(loan_application)
   

def isEligibleForLoan(loan_application):
   
     with open('scaler.pkl','rb') as f1:
         scalar_model = pickle.load(f1);
         data=scalar_model.transform([[loan_application['applicantincome'],loan_application['amountrequired']]])
         p1=data[0,0];
         p2=data[0,1];
         
     with open('logistic_loan.pkl','rb') as f:
          
       
       loans_model = pickle.load(f)
       pridiction_result =loans_model.predict([[loan_application["gender"],loan_application["married"],loan_application["dependents"],loan_application["education"],p1,p2,loan_application['credithistory'],loan_application['propertyarea']]])  
          
       return str(pridiction_result[0])