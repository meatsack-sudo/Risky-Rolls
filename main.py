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
    roll_once = SubmitField('Roll Once')
    roll_all = SubmitField('To the death!')

@app.route("/", methods=["GET", "POST"])
def home():
    form = RiskRolls()
    attackers = form.attackers.data
    defenders = form.defenders.data
    if form.validate_on_submit():
        print(f"Attackers: {attackers}. Defenders: {defenders}")
    else:
        print(Exception)
    return render_template("index.html", form=form)

def roll_dice(num_attackers, num_defenders):
    if num_attackers - 1 % 3:
        attack_dice = 3
    elif num_attackers == 3:
        attack_dice = 2
    elif num_attackers == 2:
        attack_dice = 1
    else:
        attacks_done = True

    if num_defenders >= 2:
        defend_dice = 2
    elif num_defenders == 1:
        defend_dice = 1
    else:
        defends_done = True

    if not attacks_done and not def88ends_done:
        for range(1, attack_dice)

if __name__ == '__main__':
    app.run(debug=True)