import json, datetime

from flask import Flask, render_template, request, redirect, flash, url_for

from utils import string_to_datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    failmessage = request.args.get('failmessage')
    if failmessage:
        return render_template('index.html', failmessage=failmessage)
    return render_template('index.html', failmessage=None)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if club:
        return render_template('welcome.html',club=club[0],competitions=competitions)
    return redirect(url_for('index') + '?failmessage=Sorry, that email wasn\'t found')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        places_maximum = min([12, int(foundCompetition['numberOfPlaces']), int(foundClub['points'])])
        return render_template('booking.html',club=foundClub,competition=foundCompetition, places_maximum=places_maximum)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_maximum = min([12, int(competition['numberOfPlaces']), int(club['points'])])
    try:
        placesRequired = int(request.form['places'])
    except:
        if request.form.get('places') == '' or request.form.get('places') == None:
            placesRequired = 0
        else:
            flash(f'({request.form.get("places")}) is not an allowed value !')
            return render_template('booking.html', club=club, competition=competition, places_maximum=places_maximum), 403
    if placesRequired > 12:
        flash('You can\'t book more than 12 places !')
        return render_template('booking.html', club=club, competition=competition, places_maximum=places_maximum), 403
    elif placesRequired > int(competition['numberOfPlaces']):
        flash(f'You can\'t book more than the total of available places ({competition["numberOfPlaces"]}) !')
        return render_template('booking.html', club=club, competition=competition, places_maximum=places_maximum), 403
    elif placesRequired > int(club['points']):
        flash(f'You can\'t book more than your total of points ({club["points"]}) !')
        return render_template('booking.html', club=club, competition=competition, places_maximum=places_maximum), 403
    elif string_to_datetime(competition['date']) < datetime.datetime.now():
        flash(f'You can\'t book on a past competition !')
        return render_template('booking.html', club=club, competition=competition, places_maximum=places_maximum), 403
    club['points'] = int(club['points'])-placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash(f'Great-booking complete ({placesRequired} booked) !')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))