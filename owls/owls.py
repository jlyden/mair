import functools
import owls.helpers.helpers as helpers
import owls.helpers.sqlhelpers as sql
from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)

bp = Blueprint('owls', __name__, url_prefix='/owls')

@bp.before_app_request
def load_current_game():
    game_id = session.get('game_id')

    if game_id is None:
        g.user = None
    else:
        g.user = sql.getOwlByGameId(game_id)


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

@bp.route('/resume', methods=(['GET']))
def resume():
    if request.args is None:
        flash('You must select an owl to resume the game.')
        return render_template('owls/list.html')
    else:
        # Find game
        game_id = sql.getGameByOwl(request.args.get('owl_id'))

        # Initiate session
        session.clear()
        session['game_id'] = game_id
        return redirect(url_for('owls.state'))


@bp.route('/state')
def state():
    if g.user:
        owl_nom = g.user['nom']
        owl_life = g.user['life']
        today = sql.getDay(session['game_id'])
        return render_template('owls/state.html', owl_nom=owl_nom, owl_life=owl_life, day=today)
    else:
        return redirect(url_for('owls.start'))

@bp.route('/list')
def list():
    all_owls = sql.getAllOwls()
    return render_template('owls/list.html', all_owls=all_owls)
