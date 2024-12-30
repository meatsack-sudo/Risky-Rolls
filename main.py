import random
import secrets
import os
from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import logging

logging.basicConfig(level=logging.DEBUG)



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
bootstrap = Bootstrap5(app)

class RiskRolls(FlaskForm):
    attackers = IntegerField('Attackers', validators=[NumberRange(min=2, max=250, message="Must have at least 2 attackers")])
    defenders = IntegerField('Defenders', validators=[NumberRange(min=1, max=250, message="Must have at least 1 defender")])
    roll_once = SubmitField('Roll Once')
    roll_all = SubmitField('To the death!')

@app.route("/", methods=["GET", "POST"])
def home():
    form = RiskRolls()
    attackers = None
    defenders = None
    remaining_attackers = 0
    remaining_defenders = 0
    result_message = None
    attackers_dice = None
    defenders_dice = None
    to_the_death_flag = False  # Default to False
    history = []

    if form.validate_on_submit():
        attackers = form.attackers.data
        defenders = form.defenders.data

        # Validate initial input
        if attackers < 2 or defenders < 1:
            result_message = "Invalid input: At least 2 attackers and 1 defender are required."
            return render_template(
                "index.html",
                form=form,
                result_message=result_message,
                history=[],
                to_the_death_flag=False,
                attackers_dice=[],
                defenders_dice=[]
            )

        # "Roll Once" Logic
        if form.roll_once.data:
            attacks_won, defends_won, attackers_dice, defenders_dice = roll_dice(attackers, defenders)
            remaining_attackers = max(0, attackers - defends_won)
            remaining_defenders = max(0, defenders - attacks_won)
            history.append({
                    "attacks_won": attacks_won,
                    "defends_won": defends_won,
                    "attackers_dice": attackers_dice,
                    "defenders_dice": defenders_dice,
                    "remaining_attackers": remaining_attackers,
                    "remaining_defenders": remaining_defenders
                })
            result_message = f"After one roll: {remaining_attackers} attackers and {remaining_defenders} defenders remain."

        # "To the death!" Logic
        elif form.roll_all.data:
            to_the_death_flag = True
            remaining_attackers = attackers
            remaining_defenders = defenders

            while remaining_attackers > 1 and remaining_defenders > 0: 
                attacks_won, defends_won, attackers_dice, defenders_dice = roll_dice(remaining_attackers, remaining_defenders)
                remaining_attackers = max(0, remaining_attackers - defends_won)
                remaining_defenders = max(0, remaining_defenders - attacks_won)
                history.append({
                    "attacks_won": attacks_won,
                    "defends_won": defends_won,
                    "attackers_dice": attackers_dice,
                    "defenders_dice": defenders_dice,
                    "remaining_attackers": remaining_attackers,
                    "remaining_defenders": remaining_defenders
                })
                logging.debug(f"Attack computed. Remaining attackers: {remaining_attackers}, remaining defenders: {remaining_defenders}")

            logging.debug(f"No more attacks to do. Remaining attackers: {remaining_attackers}, remaining defenders: {remaining_defenders}")
            result_message = f"After rolling to the death {remaining_attackers} attackers and {remaining_defenders} defenders remain."

    return render_template(
        "index.html",
        form=form,
        result_message=result_message,
        remaining_attackers=remaining_attackers,
        remaining_defenders=remaining_defenders,
        attackers_dice=attackers_dice,
        defenders_dice=defenders_dice,
        to_the_death_flag=to_the_death_flag,
        history=history
    )

#Random page explanation
@app.route("/how_random", methods=["GET"])
def how_random():
    return render_template(
        "how_random.html"
    )

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
        attack_rolls = [secrets.choice(range(1, 7)) for _ in range(attack_dice)]
        defense_rolls = [secrets.choice(range(1, 7)) for _ in range(defend_dice)]
        attack_rolls.sort(reverse=True)
        defense_rolls.sort(reverse=True)
        logging.debug(f"Attack rolls: {attack_rolls}, Defense rolls: {defense_rolls}")

        #Logic for deciding who won each attack:
        if defense_rolls[0] >= attack_rolls[0]:
            logging.debug(f"Defense won first roll ({defense_rolls[0]} >= {attack_rolls[0]})")
            defends_won += 1
        else:
            attacks_won += 1
            logging.debug(f"Attackers won first roll ({attack_rolls[0]} > {defense_rolls[0]})")

        if len(defense_rolls) > 1 and len(attack_rolls) > 1:
            if defense_rolls[1] >= attack_rolls[1]:
                logging.debug(f"Defense won second roll ({defense_rolls[1]} >= {attack_rolls[1]})")
                defends_won += 1
            else:
                logging.debug(f"Attackers won second roll ({attack_rolls[1]} > {defense_rolls[1]})")
                attacks_won += 1            
    else:
        logging.debug("Not enough dice to roll")
    
    return attacks_won, defends_won, attack_rolls, defense_rolls



#roll_dice(5, 3)


        

if __name__ == '__main__':
    app.run()