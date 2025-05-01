from flask import Blueprint, render_template, request, redirect, url_for, flash
from applications.models import Competition, Dataset
from applications.database import db
from applications.firebase_auth import auth_required, get_current_user

competitions_bp = Blueprint('competitions', __name__)

@competitions_bp.route('/competitions')
def list_competitions():
    competitions = Competition.query.all()
    return render_template('competitions/list.html', competitions=competitions)

@competitions_bp.route('/competitions/new', methods=['GET', 'POST'])
@auth_required
def create_competition():
    current_user = get_current_user()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        dataset_id = request.form.get('dataset_id')
        new_competition = Competition(
            title=title,
            description=description,
            deadline=deadline,
            dataset_id=dataset_id
        )
        db.session.add(new_competition)
        db.session.commit()
        flash('Competition created successfully!', 'success')
        return redirect(url_for('competitions.list_competitions'))

    datasets = Dataset.query.all()
    return render_template('competitions/create.html', datasets=datasets)

@competitions_bp.route('/competitions/<int:competition_id>')
def view_competition(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    return render_template('competitions/view.html', competition=competition)

@competitions_bp.route('/competitions/<int:competition_id>/submit', methods=['GET', 'POST'])
@auth_required
def submit_to_competition(competition_id):
    current_user = get_current_user()
    competition = Competition.query.get_or_404(competition_id)

    if request.method == 'POST':
        if 'submission_file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['submission_file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        # Placeholder for file saving logic
        flash('Submission successful!', 'success')
        return redirect(url_for('competitions.view_competition', competition_id=competition_id))

    return render_template('competitions/submit.html', competition=competition)
