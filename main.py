import math
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)

class RiskRolls(FlaskForm):
    attackers = IntegerField('Attackers', validators=[DataRequired()])
    defenders = IntegerField('Defenders', validators=[DataRequired()])
    roll_once = SubmitField('Roll_once')
    roll_all = SubmitField('Roll_all')

@app.route("/", methods=["GET", "POST"])
def home():
    form = RiskRolls()
    attackers = form.attackers.data
    defenders = form.defenders.data
    if form.validate_on_submit():
        pass
    return render_template("index.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)