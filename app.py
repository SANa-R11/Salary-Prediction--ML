from flask import Flask,render_template, request
import pickle

app=Flask(__name__)

with open("rf_salary_model.pkl","rb")as file:
    salary_model=pickle.load(file)

with open("lb_salary.pkl","rb")as file:
    lb_salary=pickle.load(file)

with open("lb1_salary.pkl","rb")as file:
    lb1_salary=pickle.load(file)

def salaryPrediction(Age=33, Gender="Female", Education_Level="Bachelor's Degree", Job_Title="Software Engineer", Years_of_Experience=3):
    lst=[]

    lst=lst+[Age]

    if Gender=="Female":
        lst=lst+[0]
    elif Gender=="Male":
        lst=lst+[1]
    elif Gender=="Other":
        lst=lst+[2]

    Education_Level=lb1_salary.transform([Education_Level])
    lst=lst+list(Education_Level)

    Job_Title=lb_salary.transform([Job_Title])
    lst=lst+list(Job_Title)

    lst=lst+[Years_of_Experience]

    
    result=salary_model.predict([lst])
    return result[0]

@app.route("/",methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/about",methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/predict",methods=["GET", "POST"])
def predict():
    if request.method== "POST":
        age=float(request.form.get("age"))
        gender=request.form.get("gender")
        education=request.form.get("education")
        job_title=request.form.get("job_title")
        experience=float(request.form.get("experience"))

        result= salaryPrediction(Age=age, Gender=gender, Education_Level=education, Job_Title=job_title, Years_of_Experience=experience)

        return render_template("predict.html", prediction=result)
    return render_template("predict.html")
@app.route("/contact",methods=["GET"])
def contact():
    return render_template("contact.html")


if __name__=="__main__":
    app.run(debug=True)