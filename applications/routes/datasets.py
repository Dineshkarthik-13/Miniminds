from flask import Blueprint, render_template, request, redirect, url_for, flash
from applications.models import Dataset
from applications.database import db
from applications.firebase_auth import auth_required, get_current_user

datasets_bp = Blueprint('datasets', __name__)

@datasets_bp.route('/datasets')
def list_datasets():
    datasets = Dataset.query.all()
    return render_template('datasets/list.html', datasets=datasets)

@datasets_bp.route('/datasets/new', methods=['GET', 'POST'])
@auth_required
def create_dataset():
    current_user = get_current_user()
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_dataset = Dataset(name=name, description=description, user_id=current_user.id)
        db.session.add(new_dataset)
        db.session.commit()
        flash('Dataset created successfully!', 'success')
        return redirect(url_for('datasets.list_datasets'))
    return render_template('datasets/create.html')

@datasets_bp.route('/datasets/<int:dataset_id>')
def view_dataset(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    return render_template('datasets/view.html', dataset=dataset)
