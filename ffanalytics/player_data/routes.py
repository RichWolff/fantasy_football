from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from ffanalytics import db
from flask import current_app
from ffanalytics.user.forms import UpdateAccountForm, UserNoteForm
from flask_login import current_user, login_required
import datetime as dt
import secrets
import os
from PIL import Image
from ffanalytics.player_data.forms import PlayerSearchForm

player_data = Blueprint('player_data', __name__)

## IMPORT DB MODEL
from ffanalytics.models import stadium_details, team_details, player_details,user_player_views

@login_required
@player_data.route('/players/<int:id>', methods=['GET', 'POST'])
def player_info(id):
    player = player_details.query.get_or_404(id)
    if current_user.is_authenticated:
        new_player_view = user_player_views(
            user_id=current_user.id,
            player_id=id)
        db.session.add(new_player_view)
        db.session.commit()
    return render_template('players/player_info.html', title = player.name + ' Information', player=player )

@login_required
@player_data.route('/players/search', methods=['GET', 'POST'])
def player_search():
    search_form = PlayerSearchForm()

    if search_form.validate_on_submit():
        player_name_search = search_form.player_name.data
        player_position_search = search_form.position.data
        player_team_search = search_form.team.data

        filters = []

        if not player_name_search == '':
            filters.append(player_details.name.contains(player_name_search))

        if not player_position_search == '':
            filters.append(player_details.position.contains(player_position_search))

        if not player_team_search == '':
            filters.append(team_details.full_name.contains(player_team_search))

        players = db.session.query(player_details).join(team_details).filter(db.and_(*filters)).all()

        return render_template('players/player_search.html', title = 'Player Search', form=search_form, players=players)


    return render_template('players/player_search.html', title = 'Player Search', form=search_form)