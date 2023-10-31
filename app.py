
from flask import Flask, request, render_template, redirect, flash
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

survey = surveys['satisfaction']
num_questions = len(survey.questions)
responses = []

app = Flask(__name__)
app.config['SECRET-KEY'] = 'foo'
app.secret_key = 'foo'
# debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    print(survey);
    return(render_template('home.html', title=survey.title))

@app.route('/questions/<int:q_ind>')
""" ask question number 'q_ind'+1 """
def question_n(q_ind):
    if (len(responses) >= num_questions):   # got enough responses, thanks!
        return redirect("/thankyou", code=302)
    elif (q_ind != len(responses)):       # somehow got on wrong page, redirect w/msg
        flash("(You've been redirected to proper next question)");
        return redirect(f"/questions/{len(responses)}", code=302)
    else:   
        return render_template('question.html', title=survey.title, question_num=q_ind+1, question=survey.questions[q_ind].question,
                            choices=survey.questions[q_ind].choices)

@app.route('/answer', methods=['POST'])
""" POST route for answer given, add to responses & redirect to next question """
def answer():
    responses.append(request.form['answer'])
 #   print(request.form['answer'])
    q_ind = len(responses)
 #   print(responses, q_ind, num_questions)
    if (q_ind < num_questions):
        return redirect(f"/questions/{q_ind}", code=302)
    else:
        return redirect("/thankyou", code=302)

@app.route('/thankyou')
""" All done, put up thanks page """
def thankyou():
    return(render_template('thankyou.html', title=survey.title))
