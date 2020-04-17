from flask import Flask, render_template, session, redirect, request
import pickle
import numpy as np

from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField
from wtforms.validators import NumberRange
import numpy as np 
from tensorflow.keras.models import load_model
import joblib


#returning prediction
def return_prediction(model,sample_json):
    
    inpt1=sample_json['tinp1']
    inpt2=sample_json['tinp2']
    inpt3=sample_json['tinp3']    
    inpt4=sample_json['tinp4']
    inpt5=sample_json['tinp5']
    inpt6=sample_json['tinp6']
    inpt7=sample_json['tinp7']
    inpt8=sample_json['tinp8']
    inpt9=sample_json['tinp8']
    inpt10=sample_json['tinp10']
    inpt11=sample_json['tinp11']
    inpt12=sample_json['tinp12']
    inpt13=sample_json['tinp13']
    inpt14=sample_json['tinp14']
    
    score=[[inpt1,inpt2,inpt3,inpt4,inpt5,inpt6,inpt7,inpt8,inpt9,inpt10,inpt11,inpt12,inpt13,inpt14]]
 
    final=[np.array(score)]
    final=np.array(final)
    final=np.squeeze(final,axis=0)
    
    prediction=model.predict(final)
    output='{0:.{1}f}'.format(prediction[0], 1)
    output=float(output)
    
    return output
    
app = Flask(__name__)

# Configure a secret SECRET_KEY
app.config['SECRET_KEY'] = 'someRandomKey'

#Loading the model
final_model=pickle.load(open('model.pkl','rb'))


#creating a WTFORM class
class scores(FlaskForm):
    inp1=TextField('tinp1')
    inp2=TextField('tinp2')
    inp3=TextField('tinp3')    
    inp4=TextField('tinp4')
    inp5=TextField('tinp5')
    inp6=TextField('tinp6')
    inp7=TextField('tinp7')
    inp8=TextField('tinp8')
    inp9=TextField('tinp8')
    inp10=TextField('tinp10')
    inp11=TextField('tinp11')
    inp12=TextField('tinp12')
    inp13=TextField('tinp13')
    inp14=TextField('tinp14')
    submit =SubmitField('Analyze')    
    
@app.route('/' , methods=['GET', 'POST'])
def index():
    form=scores()
    
    if form.validate_on_submit():
        # Grab the data from the input on the form.
        session['inp1'] = form.inp1.data
        session['inp2'] = form.inp2.data
        session['inp3'] = form.inp3.data
        session['inp4'] = form.inp4.data
        session['inp5'] = form.inp5.data
        session['inp6'] = form.inp6.data
        session['inp7'] = form.inp7.data
        session['inp8'] = form.inp8.data
        session['inp9'] = form.inp9.data
        session['inp10'] = form.inp10.data
        session['inp11'] = form.inp11.data
        session['inp12'] = form.inp12.data
        session['inp13'] = form.inp13.data
        session['inp14'] = form.inp14.data
        
        return redirect(url_for("prediction"))
    return render_template('bookie.html', form=form)
 

@app.route('/prediction')
def prediction():
    
    
    content={}
    
    content['tinp1']=float(session['inp1'])
    content['tinp2']=float(session['inp2'])
    content['tinp3']=float(session['inp3'])
    content['tinp4']=float(session['inp4'])
    
    content['tinp5']=float(session['inp5'])
    content['tinp6']=float(session['inp6'])
    content['tinp7']=float(session['inp7'])
    content['tinp8']=float(session['inp8'])
    
    content['tinp9']=float(session['inp9'])
    content['tinp10']=float(session['inp10'])
    content['tinp11']=float(session['inp11'])
    content['tinp12']=float(session['inp12'])
    
    content['tinp13']=float(session['inp13'])
    content['tinp14']=float(session['inp14'])
    
    output = return_prediction(model=final_model,sample_json=content)
    
    if output<(0.5):
        return render_template('prediction.html',pred='Home team won')
    elif output<(1.5):
        return render_template('prediction.html',pred='Away team won')
    elif output<(2.5):
        return render_template('prediction.html',pred='Match Draw')
  
    
    

    
app.run(debug=True, use_reloader=False)