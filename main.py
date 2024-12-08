import random
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
    attackers = None
    defenders = None
    result_message = None  # To display the results

    if form.validate_on_submit():
        attackers = form.attackers.data
        defenders = form.defenders.data

        if form.roll_once.data:  # "Roll Once" button clicked
            attacks_won, defends_won = roll_dice(attackers, defenders)
            remaining_attackers = max(0, attackers - defends_won)
            remaining_defenders = max(0, defenders - attacks_won)
            result_message = f"After one roll: {remaining_attackers} attackers and {remaining_defenders} defenders remain."

        elif form.roll_all.data:  # "To the death!" button clicked
            remaining_attackers, remaining_defenders = roll_dice(attackers, defenders)
            result_message = f"After rolling 'To the death': {remaining_attackers} attackers and {remaining_defenders} defenders remain."

    return render_template("index.html", form=form, result_message=result_message, remaining_attackers=remaining_attackers, remaining_defenders=remaining_defenders)

import random

def roll_dice(num_attackers, num_defenders):
    # Determine number of attack dice (max 3, but attackers need at least 2 to attack)
    if num_attackers >= 4:
        attack_dice = 3
    elif num_attackers == 3:
        attack_dice = 2
    elif num_attackers == 2:
        attack_dice = 1
    else:
        attack_dice = 0  # Not enough attackers to roll dice
    attacks_done = attack_dice == 0

    # Determine number of defense dice (max 2)
    if num_defenders >= 2:
        defend_dice = 2
    elif num_defenders == 1:
        defend_dice = 1
    else:
        defend_dice = 0  # No defenders left
    defends_done = defend_dice == 0

    if not attacks_done and not defends_done:
        attacks_won = 0
        defends_won = 0
        attack_rolls = [random.randint(1, 6) for _ in range(attack_dice)]
        defense_rolls = [random.randint(1, 6) for _ in range(defend_dice)]
        attack_rolls.sort(reverse=True)
        defense_rolls.sort(reverse=True)
        print(f"Attack rolls: {attack_rolls}, Defense rolls: {defense_rolls}")

        #Logic for deciding who won each attack:
        if defense_rolls[0] >= attack_rolls[0]:
            print(f"Defense won first roll ({defense_rolls[0]} >= {attack_rolls[0]})")
            defends_won += 1
        else:
            attacks_won += 1
            print(f"Attackers won first roll ({attack_rolls[0]} > {defense_rolls[0]})")

        if len(defense_rolls) > 1 and len(attack_rolls) > 1:
            if defense_rolls[1] >= attack_rolls[1]:
                print(f"Defense won second roll ({defense_rolls[1]} >= {attack_rolls[1]})")
                defends_won += 1
            else:
                print(f"Attackers won second roll ({attack_rolls[1]} > {defense_rolls[1]})")
                attacks_won += 1            

    else:
        print("Not enough dice to roll")
    
    return attacks_won, defends_won



#roll_dice(5, 3)


        

if __name__ == '__main__':
    app.run(debug=True)