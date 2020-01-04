from flask import session, render_template, flash, redirect, url_for, request

from app import app
from app import db
from . constant import *
from . models import Owl, World

@app.route('/')
@app.route('/index')
def index():
    return "This is a sanity check."


@app.route('/start', methods=(['GET','POST']))
def start():
    if request.method == 'POST':
        nom = request.form['nom']
        error = None

        # Validate form
        if not nom:
            error = 'You must name your owl.'
        elif Owl.query.filter_by(nom=nom).first() is not None:
            error = 'Owl {} has already started playing.'.format(nom)
        
        if error is None:
            # Set up game
            new_owl = Owl(nom=nom)
            db.session.add(new_owl)
            db.session.commit()
            print('in start, new_owl.nom is ' + new_owl.nom)
            new_world = World(owl_id=new_owl.id)
            db.session.add(new_world)
            db.session.commit()
            print('in start, new_world.mouse_pop is ' + str(new_world.mouse_pop))

            # Initiate session
            session.clear()
            session['world_id'] = new_world.id
            return redirect(url_for('state'))

        flash(error)
    return render_template('app/start.html')


@app.route('/list')
def list():
    all_owls = Owl.query.all()
    if all_owls == None:
        flash("There's no owls yet! Create one.")
        return redirect(url_for('start'))
    else: 
        return render_template('app/list.html', owls=all_owls)


@app.route('/resume')
def resume():
    owl_id = request.args.get('owl_id')
    print('in resume, owl_id is ' + str(owl_id))
    if owl_id is None:
        flash('You must select an owl to resume the game.')
        return redirect(url_for('list'))
    else:
        # Find game
        owl_id = int(owl_id)
        this_world = World.query.filter_by(owl_id=owl_id).first()
        print('in resume, this_world.id is ' + str(this_world.id))

        # Initiate session
        session.clear()
        session['world_id'] = this_world.id
        return redirect(url_for('state'))


@app.route('/state')
def state():
    world_id = session.get('world_id')
    print('in state, world_id is ' + str(world_id))
    this_world = World.query.get(world_id)
    print('in state, this_world.id from db is ' + str(this_world.id))
    if this_world:
        this_owl = Owl.query.get(this_world.owl_id)
        print('in state, this_owl.id from db is ' + str(this_owl.id))
        return render_template('app/state.html', owl=this_owl, world=this_world)
    else:
        flash(MSG_NO_ACTIVE_GAME)
        return redirect(url_for('start'))


@app.route('/sleep')
def sleep():
    world_id = session.get('world_id')
    owl_id = request.args.get('owl_id')
    this_owl = Owl.query.get(owl_id)
    if this_owl:
        this_owl = this_owl.sleep()
        return redirect(url_for('state'))
    else:
        flash(MSG_NO_ACTIVE_GAME)
        return redirect(url_for('start'))


@app.route('/eat')
def eat():
    message = None
    world_id = session.get('world_id')
    owl_id = request.args.get('owl_id')
    this_owl = Owl.query.get(owl_id)
    if this_owl:
        this_owl, message = this_owl.eat()
        this_world = World.query.get(world_id)
        this_world.checkAndHandleEndOfDay(this_owl)
        flash(message)
        return redirect(url_for('state'))
    else:
        flash(MSG_NO_ACTIVE_GAME)
        return redirect(url_for('start'))


@app.route('/hunt')
def hunt():
    world_id = session.get('world_id')
    owl_id = request.args.get('owl_id')
    this_owl = Owl.query.get(owl_id)
    if this_owl:
        this_world = World.query.get(world_id)
        this_owl, this_world, message = this_owl.hunt(this_world)
        this_world.checkAndHandleEndOfDay(this_owl)
        flash(message)
        return redirect(url_for('state'))
    else:
        flash(MSG_NO_ACTIVE_GAME)
        return redirect(url_for('start'))
