
from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

survey = surveys['satisfaction']
num_questions = len(survey.questions)

app = Flask(__name__)
app.config['SECRET-KEY'] = 'foo'
app.secret_key = 'foo'
# debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    print(survey)
    return(render_template('home.html', title=survey.title))

@app.route('/questions/<int:q_ind>',methods=['GET'])
def question_n(q_ind):
    """ ask question number 'q_ind'+1 """
    print(session['responses'])
    responses = session['responses']
    if (len(responses) >= num_questions):   # got enough responses, thanks!
        return redirect("/thankyou", code=302)
    elif (q_ind != len(responses)):       # somehow got on wrong page, redirect w/msg
        flash("(You've been redirected to the next question)");
        return redirect(f"/questions/{len(responses)}", code=302)
    else:   
        return render_template('question.html', title=survey.title, question_num=q_ind+1, question=survey.questions[q_ind].question,
                            choices=survey.questions[q_ind].choices)

@app.route('/questions/0',methods=['POST'])
def question_0():
    """ 1st question, got sent here from 'begin survey' """
    session['responses'] = []
    return render_template('question.html', title=survey.title, question_num=1, question=survey.questions[0].question,
                        choices=survey.questions[0].choices)

@app.route('/answer', methods=['POST'])
def answer():
    """ POST route for answer given, add to responses & redirect to next question """
    responses = session['responses']
    responses.append(request.form['answer'])
    session['responses'] = responses
    q_ind = len(responses)
    if (q_ind < num_questions):
        return redirect(f"/questions/{q_ind}", code=302)
    else:
        return redirect("/thankyou", code=302)

@app.route('/thankyou')
def thankyou():
    """ All done, put up thanks page """
    print(session['responses'])
    return(render_template('thankyou.html', title=survey.title))
