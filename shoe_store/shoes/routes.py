from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from shoe_store.extensions import db
from shoe_store.models import Shoe, User, Category
from flask_login import current_user, login_required

shoe_bp = Blueprint('shoe', __name__, template_folder='templates')

@shoe_bp.route('/')
@login_required
def index():
    query = db.select(Shoe).where(Shoe.user == current_user)
    shoes = db.session.scalars(query).all()
    return render_template('shoes/index.html', title='My Shoes', shoes=shoes)

@shoe_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_shoe():
    shoe_categories = db.session.scalars(db.select(Category)).all()
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        img_url = request.form.get('img_url')
        category_ids = request.form.getlist('shoe_categories')
        user_id = current_user.id

        cats = []
        for cid in category_ids:
            cats.append(db.session.get(Category, int(cid)))

        shoe = Shoe(
            name=name,
            price=price,
            description=description,
            img_url=img_url,
            user_id=user_id,
            categories=cats
        )
        db.session.add(shoe)
        db.session.commit()
        flash(f'เพิ่มรายการรองเท้า {name} เรียบร้อยแล้ว', 'success')
        return redirect(url_for('shoe.index'))

    return render_template('shoes/new_shoe.html', title='เพิ่มรองเท้า', shoe_categories=shoe_categories)

@shoe_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_shoe(id):
    shoe = db.session.get(Shoe, id)
    if not shoe:
        abort(404)
    if shoe.user_id != current_user.id:
        abort(403)

    shoe_categories = db.session.scalars(db.select(Category)).all()
    if request.method == 'POST':
        shoe.name = request.form.get('name')
        shoe.price = request.form.get('price')
        shoe.description = request.form.get('description')
        shoe.img_url = request.form.get('img_url')
        category_ids = request.form.getlist('shoe_categories')

        cats = []
        for cid in category_ids:
            cats.append(db.session.get(Category, int(cid)))
        shoe.categories = cats

        db.session.commit()
        flash(f'แก้ไขข้อมูลรองเท้า {shoe.name} เรียบร้อยแล้ว', 'success')
        return redirect(url_for('shoe.index'))

    return render_template('shoes/edit_shoe.html', title='แก้ไขรองเท้า', shoe=shoe, shoe_categories=shoe_categories)

@shoe_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_shoe(id):
    shoe = db.session.get(Shoe, id)
    if not shoe:
        abort(404)
    if shoe.user_id != current_user.id:
        abort(403)

    shoe_name = shoe.name
    db.session.delete(shoe)
    db.session.commit()
    flash(f'ลบรายการรองเท้า {shoe_name} เรียบร้อยแล้ว', 'success')
    return redirect(url_for('shoe.index'))

@shoe_bp.route('/search')
def search():
    q = request.args.get('q', '')
    shoes = []
    if q:
        query = db.select(Shoe).where(Shoe.name.ilike(f'%{q}%'))
        shoes = db.session.scalars(query).all()
    return render_template('shoes/search_results.html', title='Search', shoes=shoes, q=q)

@shoe_bp.route('/search-live')
def search_live():
    q = request.args.get('q', '')
    shoes = []
    if q and len(q) >= 1:
        query = db.select(Shoe).where(Shoe.name.ilike(f'%{q}%')).limit(5)
        shoes = db.session.scalars(query).all()
    return render_template('shoes/search_dropdown.html', shoes=shoes, q=q)
