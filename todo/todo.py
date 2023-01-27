from flask import (

	Blueprint,
	flash,
	g,
	redirect,
	render_template,
	request,
	url_for

)
from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__, template_folder='../templates')


@bp.route('/')
@login_required
def index():
	db, c = get_db()
	c.execute(
		'select t.id, t.description, u.username, t.completed, t.created_ad from todo t JOIN users u on t.created_by = u.id order by created_ad desc'
	)
	todos = c.fetchall()

	return render_template('todo/index.html', todos=todos)