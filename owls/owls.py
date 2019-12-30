import functools
import owls.helpers.helpers as helpers
import owls.helpers.sqlhelpers as sql
from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)

bp = Blueprint('owls', __name__, url_prefix='/owls')

@bp.route('/start', methods=(['GET','POST']))
def start():
    if request.method == 'POST':
        nom = request.form['nom']
        error = helpers.validateStart(nom)
        
        if error is None:
            # Set up game
            game_id = helpers.initiateGame(nom)

            # Initiate session
            session.clear()
            session['game_id'] = game_id
            return redirect(url_for('owls.state'))

        flash(error)

    return render_template('owls/start.html')

@bp.route('/resume')
def resume():
    if request.args.get('owl_id') is None:
        flash('You must select an owl to resume the game.')
        return redirect(url_for('owls.list'))
    else:
        # Find game
        owl_id = int(request.args.get('owl_id'))
        game_id = sql.getGameIdByOwlId(owl_id)

        # Initiate session
        session.clear()
        session['game_id'] = game_id
        return redirect(url_for('owls.state'))


@bp.route('/state')
def state():
    this_owl = helpers.getOwl(session.get('game_id'))
    if this_owl:
        today = sql.getDay(session['game_id'])
        return render_template('owls/state.html', owl=this_owl, day=today)
    else:
        flash('no active game - please create an owl or select from list')
        return redirect(url_for('owls.start'))

@bp.route('/list')
def list():
    all_owls = helpers.getAllOwls()
    return render_template('owls/list.html', all_owls=all_owls)
