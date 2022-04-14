from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import defaultload
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class FeedbackForm(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile_no = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.name}'


@app.route("/")
def hello_world():
    return render_template('/about.html')

# @app.route("/list-feedbacks")
# def feedback_list():
#     feedbacks  = FeedbackForm.query.all()
#     print(feedbacks)
#     return "<p>Hello, Test!</p>"


@app.route("/delete/<int:sno>/")
def feedback_delete(sno):
    feedback  = FeedbackForm.query.filter_by(sno=sno).first()
    db.session.delete(feedback)
    db.session.commit()
    allfeedbacks  = FeedbackForm.query.all()
    print(allfeedbacks)
    return redirect('/contact')

@app.route('/update/<int:sno>/', methods=['GET','POST'])
def feedback_update(sno):
    if request.method=='POST':
        name = request.form['name']
        mobile_no = request.form['mobile_no']
        email = request.form['email']
        title = request.form['title']
        desc = request.form['desc']
        feedback = FeedbackForm.query.filter_by(sno=sno).first()
        feedback.name = name
        feedback.mobile_no = mobile_no
        feedback.email = email
        feedback.title = title
        feedback.desc = desc
        db.session.add(feedback)
        db.session.commit()
        return redirect("/contact/")
        
    feedback = FeedbackForm.query.filter_by(sno=sno).first()
    return render_template('/update.html', feedback=feedback)


@app.route("/contact/", methods=['GET', 'POST'])
def about_me():
    if request.method == 'POST':
        name = request.form['name']
        mobile_no = request.form['mobile_no']
        email = request.form['email']
        title = request.form['title']
        desc = request.form['desc']
        form = FeedbackForm(name=name, mobile_no=mobile_no, email=email, title=title, desc=desc)
        db.session.add(form)
        db.session.commit()
    allfeedbacks  = FeedbackForm.query.all()
    print(allfeedbacks)
    return render_template('/index.html', allfeedbacks=allfeedbacks)


if __name__ == "__main__":
    app.run(debug=True, port=8000)