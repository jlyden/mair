import functools
import game.helpers.helpers as helpers
import game.classes.owl as owl
import game.classes.world as world
import game.constant as const
from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)

# TODO: end/day colliding with action bonuses

bp = Blueprint('game', __name__, url_prefix='/game')

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
            return redirect(url_for('game.state'))

        flash(error)

    return render_template('game/start.html')

@bp.route('/resume')
def resume():
    if request.args.get('owl_id') is None:
        flash('You must select an owl to resume the game.')
        return redirect(url_for('game.list'))
    else:
        # Find game
        owl_id = int(request.args.get('owl_id'))
        game_id = sql.getGameIdByOwlId(owl_id)

        # Initiate session
        session.clear()
        session['game_id'] = game_id
        return redirect(url_for('game.state'))

@bp.route('/list')
def list():
    all_owls = helpers.getAllOwls()
    return render_template('game/list.html', all_owls=all_owls)

@bp.route('/state')
def state():
    game_id = session.get('game_id')
    this_owl = helpers.getOwl(game_id)
    if this_owl:
        today = world.getDay(game_id)
        mouse_pop = sql.getMousePopulation(game_id)
        return render_template('game/state.html', owl=this_owl, day=today, mice=mouse_pop)
    else:
        flash('no active game - please create an owl or select from list')
        return redirect(url_for('game.start'))

@bp.route('/sleep')
def sleep():
    game_id = session.get('game_id')
    this_owl = helpers.getOwl(game_id)
    if this_owl:
        owl.owlSleep(this_owl)
        helpers.checkAndHandleEndOfDay(game_id, this_owl)
        return redirect(url_for('game.state'))
    else:
        flash('no active game - please create an owl or select from list')
        return redirect(url_for('game.start'))

@bp.route('/eat')
def eat():
    game_id = session.get('game_id')
    this_owl = helpers.getOwl(game_id)
    if this_owl:
        message = owl.eat()
        helpers.checkAndHandleEndOfDay(game_id, this_owl)
        flash(message)
        return redirect(url_for('game.state'))
    else:
        flash('no active game - please create an owl or select from list')
        return redirect(url_for('game.start'))

@bp.route('/hunt')
def hunt():
    game_id = session.get('game_id')
    this_owl = helpers.getOwl(game_id)
    if this_owl:
        message = helpers.owlHunt(game_id, this_owl)
        helpers.checkAndHandleEndOfDay(game_id, this_owl)
        flash(message)
        return redirect(url_for('game.state'))
    else:
        flash('no active game - please create an owl or select from list')
        return redirect(url_for('game.start'))
