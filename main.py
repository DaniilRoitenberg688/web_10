from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session, job_resources, user_resources
from data.jobs import Job
from data.users import User
from forms.job import AddJobForm, EditJobForm
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app, catch_all_404s=True)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            speciality=form.jobs.data,
            age=form.age.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        jobs = db_sess.query(Job).filter((Job.team_leader == current_user.id) | (Job.is_finished != True))
    else:
        jobs = db_sess.query(Job).filter(Job.is_finished != True)
    return render_template("index.html", title='Mars Jobs', jobs=jobs)


@app.route('/jobs', methods=['GET', 'POST'])
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        job = Job(team_leader=form.team_leader.data,
                  job=form.job.data,
                  work_size=form.work_size.data,
                  collaborators=form.collaborators.data)
        db_sess = db_session.create_session()
        db_sess.merge(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_work.html', title='Add new', form=form)


@app.route('/jobs/<id>', methods=['GET', 'POST'])
def edit_job(id):
    form = EditJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        our_job = db_sess.query(Job).filter(Job.id == id).first()
        our_job.team_leader = form.team_leader.data
        our_job.job = form.job.data
        our_job.work_size = form.work_size.data
        our_job.collaborators = form.collaborators.data
        db_sess.commit()
        return redirect('/')
    return render_template('add_work.html', title='Edit job', form=form)


@app.route('/jobs_delete/<id>', methods=['GET', 'POST'])
def delete_job(id):
    db_sess = db_session.create_session()
    db_sess.query(Job).filter(Job.id == id).delete()
    db_sess.commit()
    return redirect('/')


def main():
    db_session.global_init('db/mars.db')
    api.add_resource(job_resources.JobListResource, '/api/jobs')
    api.add_resource(job_resources.JobResource, '/api/jobs/<int:job_id>')
    api.add_resource(user_resources.UserListResource, '/api/users')
    api.add_resource(user_resources.UserResource, '/api/users/<int:user_id>')
    app.run()


if __name__ == '__main__':
    main()
