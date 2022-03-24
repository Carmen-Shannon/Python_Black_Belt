from flask import redirect, render_template, session, request, flash
from flask_app import app
from flask_app.models import user, painting


@app.route('/add_painting_page')
def add_painting_page():
    try:
        if not session['current_id']:
            return redirect('/')
    except KeyError:
        return redirect('/')

    data = {'id': session['current_id']}

    current_user = user.User.get_user_by_id(data)
    return render_template('add_painting.html', user=current_user)


@app.route('/add_painting', methods=['POST'])
def add_painting():
    try:
        if not session['current_id']:
            return redirect('/')
    except KeyError:
        return redirect('/')

    if not painting.Painting.validate(request.form):
        return redirect('/add_painting_page')

    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'price': request.form['price'],
        'quantity': request.form['quantity'],
        'created_by': session['current_id']
    }

    painting.Painting.add_painting(data)
    return redirect('/dashboard')


@app.route('/view_painting/<int:id>')
def view_painting(id):
    try:
        if not session['current_id']:
            return redirect('/')
    except KeyError:
        return redirect('/')

    data = {'id': id}
    current_painting = painting.Painting.get_painting_by_id(data)
    if current_painting == False:
        return redirect('/painting_removed')
    data2 = {'id': current_painting.created_by}
    painted_by = user.User.get_user_by_id(data2)
    data3 = {'id': session['current_id']}
    current_user = user.User.get_user_by_id(data3)
    return render_template('view_painting.html', user=current_user, painting=current_painting, creator=painted_by)


@app.route('/painting_removed')
def painting_removed():
    try:
        if not session['current_id']:
            return redirect('/')
    except KeyError:
        return redirect('/')
    data = {'id': session['current_id']}
    current_user = user.User.get_user_by_id(data)
    return render_template('painting_removed.html', user=current_user)


@app.route('/remove_quantity', methods=['POST'])
def purchase():
    try:
        if not session['current_id']:
            return redirect('/')
    except KeyError:
        return redirect('/')

    data = {'id': session['current_id']}
    data2 = {'id': request.form['painting_id']}
    current_painting = painting.Painting.get_painting_by_id(data2)
    current_user = user.User.get_user_by_id(data)
    data3 = {'id': current_painting.created_by}
    current_painting.author = user.User.get_user_by_id(data3)
    data4 = {
        'id': current_painting.id,
        'quantity': int(current_painting.quantity) - 1,
        'amount_purchased': int(current_painting.amount_purchased) + 1
    }
    data5 = {
        'user_id': session['current_id'],
        'painting_id': request.form['painting_id']
    }
    painting.Painting.create_purchase(data5)
    painting.Painting.update_quantity(data4)
    return redirect(f'/view_painting/{current_painting.id}')


@app.route('/delete_painting/<int:id>')
def delete_painting(id):
    try:
        if not session['current_id']:
            return redirect('/')
    except KeyError:
        redirect('/')

    data = {'id': id}

    current_painting = painting.Painting.get_painting_by_id(data)
    if current_painting.created_by != session['current_id']:
        return redirect('/dashboard')

    painting.Painting.delete_painting(data)
    return redirect('/dashboard')


@app.route('/edit_painting/<int:id>', methods=['POST'])
def edit_painting(id):
    try:
        if not session['current_id']:
            return redirect('/')
    except KeyError:
        return redirect('/')

    if not painting.Painting.validate(request.form):
        return redirect(f'/edit_painting_page/{id}')

    data = {
        'id': id,
        'title': request.form['title'],
        'description': request.form['description'],
        'price': request.form['price'],
        'quantity': request.form['quantity']
    }
    data2 = {'id': session['current_id']}
    data3 = {'id': id}
    current_user = user.User.get_user_by_id(data2)
    current_painting = painting.Painting.get_painting_by_id(data3)

    if current_user.id != current_painting.created_by:
        return redirect('/dashboard')

    painting.Painting.update_painting(data)
    return redirect('/dashboard')


@app.route('/edit_painting_page/<int:id>')
def edit_painting_page(id):
    try:
        if not session['current_id']:
            return redirect('/')
    except KeyError:
        return redirect('/')

    data = {'id': id}
    data2 = {'id': session['current_id']}
    current_painting = painting.Painting.get_painting_by_id(data)
    painting_price = int(current_painting.price)
    painting_quantity = int(current_painting.quantity)
    current_user = user.User.get_user_by_id(data2)

    return render_template('edit_painting.html', user=current_user, creator=current_painting.author, painting=current_painting, painting_price=painting_price, painting_quantity=painting_quantity)
