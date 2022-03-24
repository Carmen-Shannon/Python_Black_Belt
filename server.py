from flask_app import app
from flask_app.controllers import paintings, users
from flask_app.models import painting, user
from flask import render_template, redirect, session


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    try:

        if not session['current_id']:
            return redirect('/')

    except KeyError:
        return redirect('/')
    data = {'id': session['current_id']}
    all_paintings = painting.Painting.get_all()
    current_user = user.User.get_user_by_id(data)

    if all_paintings:
        for each_painting in all_paintings:
            data2 = {'id': each_painting.created_by}
            each_painting.author = user.User.get_user_by_id(data2)

    owned_paintings = painting.Painting.get_paintings_by_purchased(data)
    if owned_paintings:
        for each in owned_paintings:
            data3 = {'id': each.created_by}
            each.author = user.User.get_user_by_id(data3)

    return render_template('dashboard.html', user=current_user, paintings=all_paintings, owned_paintings=owned_paintings)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
