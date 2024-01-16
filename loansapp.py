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
         print(loan_application)
         scalar_model = pickle.load(f1);
         print("Q")
         print(loan_application['amountrequired'])
         loan_application['applicantincome']
         data=scalar_model.transform([[loan_application['applicantincome'],loan_application['amountrequired']]])
         p1=data[0,0];
         p2=data[0,1];
         
     with open('logistic_loan.pkl','rb') as f:
          
       print("P")
       loans_model = pickle.load(f)
       pridiction_result =loans_model.predict([[1,1,loan_application["dependents"],loan_application["education"],p1,p2,loan_application['credithistory'],loan_application['propertyarea']]])  
       print(str(pridiction_result[0]))
       return str(pridiction_result[0])