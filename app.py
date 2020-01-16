from flask import Flask, render_template, request, redirect
from forms.user_form import UserForm
from forms.feature_form import FeatureForm
from forms.remedy_form import RemedyForm
import json
import plotly
from sqlalchemy.sql import func
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import random as rnd
import gunicorn
from math import fabs
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans


app = Flask(__name__)
app.secret_key = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hjbywnkvkncvpp:a3995b361295f55f6c35a1fe7ddce53876fa61cd9ae9408443e95e47cac373e4@ec2-174-129-33-84.compute-1.amazonaws.com:5432/d50235egbbs33'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:fastdagger@localhost/milev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class OrmUser(db.Model):
    __tablename__ = 'orm_user'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(20), nullable=False)
    skin_condition = db.Column(db.Integer, nullable=False)
    eye_color = db.Column(db.String(20), nullable=False)
    hair_color = db.Column(db.String(20), nullable=False)
    lips_color = db.Column(db.String(20), nullable=False)
    skin_tone = db.Column(db.String(20), nullable=False)

    feature = db.relationship('OrmFeature')


class OrmFeature(db.Model):
    __tablename__ = 'orm_feature'

    feature_id = db.Column(db.Integer, primary_key=True)
    feature_name = db.Column(db.String(20), nullable=False)
    feature_size = db.Column(db.String(40), nullable=False)
    formtype = db.Column(db.String(40), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('orm_user.user_id'))

    remedy = db.relationship('OrmRemedy')

class OrmRemedy(db.Model):
    __tablename__ = 'orm_remedy'
    remedy_id = db.Column(db.Integer, primary_key=True)
    remedy_name = db.Column(db.String(20), nullable=False)
    remedy_color = db.Column(db.String(20), nullable=False)
    remedy_brightness = db.Column(db.String(20), nullable=False)

    feature_id = db.Column(db.Integer, db.ForeignKey('orm_feature.feature_id'))


# try:
#     db.drop_all()
#     db.session.commit()
# except:
#     pass

db.create_all()
# db.session.commit()

John = OrmUser(
    user_id=1,
    user_name='Olya',
    user_age=19,
    user_email='Olya@mail.com',
    skin_condition=7,
    eye_color = 'green',
    hair_color = 'brown',
    lips_color = 'saturated',
    skin_tone = 'pale'
)

Paul = OrmUser(
    user_id=2,
    user_name='Masha',
    user_age=45,
    user_email='Masha@mail.com',
    skin_condition=4,
    eye_color='brown',
    hair_color='brown',
    lips_color='unsaturated',
    skin_tone='dark'
)

George = OrmUser(
    user_id=3,
    user_name='Nastya',
    user_age=36,
    user_email='Nastya@mail.com',
    skin_condition=3,
    eye_color='blue',
    hair_color='blonde',
    lips_color='unsaturated',
    skin_tone='gray'
)

Ringo = OrmUser(
    user_id=4,
    user_name='Kate',
    user_age=81,
    user_email='Kate@mail.com',
    skin_condition=1,
    eye_color='gray',
    hair_color='blonde',
    lips_color='unsaturated',
    skin_tone='pink'
)


Paul_nose = OrmFeature(
    feature_id=1,
    feature_name='nose',
    feature_size='small',
    formtype='Aquiline nose',
    user_id=2

)

Paul_lips = OrmFeature(
    feature_id=2,
    feature_name='lips',
    feature_size='big',
    formtype='chubby, cracked',
    user_id=2

)

John_nose = OrmFeature(
    feature_id=3,
    feature_name='nose',
    feature_size='big',
    formtype='Roman nose',
    user_id=1
)

George_eyes = OrmFeature(
    feature_id=4,
    feature_name='eyes',
    feature_size='medium',
    formtype='deep, suspicious',
    user_id=3

)

Pomade = OrmRemedy(
    remedy_id = 1,
    remedy_name = 'pomade',
    remedy_color = 'red',
    remedy_brightness = 'strong',
    feature_id=2
)

Shadows = OrmRemedy(
    remedy_id = 2,
    remedy_name = 'shadows',
    remedy_color = 'brown',
    remedy_brightness = 'low',
    feature_id=4
)

Conciller = OrmRemedy(
    remedy_id = 3,
    remedy_name = 'conciller',
    remedy_color = 'ivory',
    remedy_brightness = 'low',
    feature_id = 3
)

Poudre = OrmRemedy(
    remedy_id = 4,
    remedy_name = 'poudre',
    remedy_color = 'rose',
    remedy_brightness = 'medium',
    feature_id = 1
)

# db.session.add_all([

#     John,
#     Paul,
#     George,
#     Ringo,
#     Paul_nose,
#     Paul_lips,
#     John_nose,
#     George_eyes,
#     Pomade,
#     Shadows,
#     Conciller,
#     Poudre
# ])

# db.session.commit()


@app.route('/', methods=['POST', 'GET'])
def root():
    return render_template('index.html')


@app.route('/users')
def users():
    res = db.session.query(OrmUser).all()

    return render_template('users_table.html', users=res)

@app.route('/user_details/<int:id>')
def user_details(id):
    res = db.session.query(OrmUser).filter(OrmUser.user_id == id).all()

    return render_template('user_details.html', users=res)

@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form = UserForm()
    next_id = None
    id_zero = db.session.query(OrmUser.user_id).all()
    if not id_zero:
        next_id = 1
    else:
        next_id_prep = max(db.session.query(OrmUser.user_id).all())
        next_id = next_id_prep[0] + 1
    if request.method == 'POST':
        if form.validate():
            try:
                new_user = OrmUser(
                    user_id=next_id,
                    user_name=form.user_name.data,
                    user_age=form.user_age.data,
                    user_email=form.user_email.data,
                    skin_condition=form.skin_condition.data,
                    eye_color = form.eye_color.data,
                    hair_color = form.hair_color.data,
                    lips_color = form.lips_color.data,
                    skin_tone = form.skin_tone.data
                )
                db.session.add(new_user)
                db.session.commit()
                return render_template('success.html')
            except:
                return render_template('user_form.html', form=form)
        else:
            return render_template('user_form.html', form=form)
    elif request.method == 'GET':
        return render_template('user_form.html', form=form)


@app.route('/user_edit/<string:id>', methods=['GET', 'POST'])
def edit_user(id):
    form = UserForm()
    result = db.session.query(OrmUser).filter(OrmUser.user_id == id).one()

    if request.method == 'GET':

        form.user_name.data = result.user_name
        form.user_age.data = result.user_age
        form.user_email.data = result.user_email
        form.skin_condition.data = result.skin_condition
        form.eye_color.data = result.eye_color
        form.hair_color.data = result.hair_color
        form.lips_color.data = result.lips_color
        form.skin_tone.data = result.skin_tone

        return render_template('user_form.html', form=form, form_name='edit user')
    elif request.method == 'POST':
        if form.validate():
            try:
                result.user_name = form.user_name.data
                result.user_age = form.user_age.data
                result.user_email = form.user_email.data
                result.skin_condition = form.skin_condition.data
                result.eye_color= form.eye_color.data
                result.hair_color= form.hair_color.data
                result.lips_color= form.lips_color.data
                result.skin_tone= form.skin_tone.data

                db.session.commit()
                return redirect('/users')
            except:
                return render_template('user_form.html', form=form)
        else:
            return render_template('user_form.html', form=form)

@app.route('/delete_user/<string:id>', methods=['GET', 'POST'])
def delete_user(id):
    result = db.session.query(OrmUser).filter(OrmUser.user_id == id).one()

    features_rows = db.session.query(OrmFeature).filter(OrmFeature.user_id == id).all()
    features_ids = db.session.query(OrmFeature.feature_id).filter(OrmFeature.user_id == id).all()

    feat_ids = []
    for id in features_ids:
        feat_ids.append(id[0])

    for id in feat_ids:
        rems = db.session.query(OrmRemedy).filter(OrmRemedy.feature_id == id).all()
        for row in rems:
            db.session.delete(row)

    for row in features_rows:
        db.session.delete(row)

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')
    # return render_template('r_u_sure.html')

# feature
@app.route('/features')
def features():
    res = db.session.query(OrmFeature).all()

    return render_template('features_table.html', features=res)

@app.route('/new_feature/<int:id>', methods=['GET', 'POST'])
def new_feature(id):
    form = FeatureForm()

    u_id_prep = db.session.query(OrmUser.user_id).filter(OrmUser.user_id == id).one()
    u_id = u_id_prep[0]

    next_id = None
    id_zero = db.session.query(OrmFeature.feature_id).all()
    if not id_zero:
        next_id = 1
    else:
        next_id_prep = max(db.session.query(OrmFeature.feature_id).all())
        next_id = next_id_prep[0] + 1

    if request.method == 'POST':
        if form.validate():
            try:
                new_feature = OrmFeature(
                    feature_id=next_id,
                    feature_name=form.feature_name.data,
                    feature_size=form.feature_size.data,
                    formtype=form.formtype.data,
                    user_id=u_id
                )
                db.session.add(new_feature)
                db.session.commit()
                return render_template('success.html')
            except:
                return render_template('feature_form.html', form=form)
        else:
            return render_template('feature_form.html', form=form)
    elif request.method == 'GET':
        return render_template('feature_form.html', form=form)

@app.route('/edit_feature/<string:id>', methods=['GET', 'POST'])
def edit_feature(id):
    form = FeatureForm()
    result = db.session.query(OrmFeature).filter(OrmFeature.feature_id == id).one()

    if request.method == 'GET':

        form.feature_name.data = result.feature_name
        form.feature_size.data = result.feature_size
        form.formtype.data = result.formtype

        return render_template('feature_form.html', form=form, form_name='edit feature')
    elif request.method == 'POST':

        if form.validate():
            try:
                result.feature_name = form.feature_name.data
                result.feature_size = form.feature_size.data
                result.formtype = form.formtype.data

                db.session.commit()
                return redirect('/features')
            except:
                return render_template('feature_form.html', form=form)
        else:
            return render_template('feature_form.html', form=form)



@app.route('/delete_feature/<string:id>', methods=['GET', 'POST'])
def delete_feature(id):
    result = db.session.query(OrmFeature).filter(OrmFeature.feature_id == id).one()

    remedys_rows = db.session.query(OrmRemedy).filter(OrmRemedy.feature_id == id).all()

    for row in remedys_rows:
        db.session.delete(row)

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')


# remedy
@app.route('/remedys')
def remedys():
    res = db.session.query(OrmRemedy).all()

    return render_template('remedys_table.html', remedys=res)


@app.route('/new_remedy/<int:id>', methods=['GET', 'POST'])
def new_remedy(id):
    form = RemedyForm()

    f_id_prep = db.session.query(OrmFeature.feature_id).filter(OrmFeature.feature_id == id).one()
    f_id = f_id_prep[0]

    next_id = None
    id_zero = db.session.query(OrmRemedy.remedy_id).all()
    if not id_zero:
        next_id = 1
    else:
        next_id_prep = max(db.session.query(OrmRemedy.remedy_id).all())
        next_id = next_id_prep[0] + 1

    if request.method == 'POST':
        if form.validate():
            try:
                new_remedy = OrmRemedy(
                    remedy_id=next_id,
                    remedy_name=form.remedy_name.data,
                    remedy_color=form.remedy_color.data,
                    remedy_brightness=form.remedy_brightness.data,
                    feature_id=f_id
                )
                db.session.add(new_remedy)
                db.session.commit()
                return render_template('success.html')
            except:
                return render_template('remedy_form.html', form=form)
        else:
            return render_template('remedy_form.html', form=form)
    elif request.method == 'GET':
        return render_template('remedy_form.html', form=form)


@app.route('/edit_remedy/<string:id>', methods=['GET', 'POST'])
def edit_remedy(id):
    form = RemedyForm()
    result = db.session.query(OrmRemedy).filter(OrmRemedy.remedy_id == id).one()

    if request.method == 'GET':

        form.remedy_name.data = result.remedy_name
        form.remedy_color.data = result.remedy_color
        form.remedy_brightness.data = result.remedy_brightness

        return render_template('remedy_form.html', form=form, form_name='edit remedy')
    elif request.method == 'POST':
        if form.validate():
            try:
                result.remedy_name = form.remedy_name.data
                result.remedy_color = form.remedy_color.data
                result.remedy_brightness = form.remedy_brightness.data
                db.session.commit()
                return redirect('/remedys')
            except:
                return render_template('remedy_form.html', form=form)
        else:
            return render_template('remedy_form.html', form=form)


@app.route('/delete_remedy/<string:id>', methods=['GET', 'POST'])
def delete_remedy(id):
    result = db.session.query(OrmRemedy).filter(OrmRemedy.remedy_id == id).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    my_query = (
        db.session.query(
            OrmUser.user_id,
            func.count(OrmFeature.feature_id).label('feature_count')
        ).join(OrmFeature, OrmUser.user_id == OrmFeature.user_id).
            group_by(OrmUser.user_id)
    ).all()

    re_query = (
        db.session.query(
            OrmFeature.feature_id,
            func.count(OrmRemedy.remedy_id).label('remedy_count')
        ).join(OrmRemedy, OrmRemedy.feature_id == OrmFeature.feature_id).
            group_by(OrmFeature.feature_id)
    ).all()


    user_id, feature_count = zip(*my_query)

    bar = go.Bar(
        x=user_id,
        y=feature_count
    )

    feature_id, remedy_count = zip(*re_query)
    pie = go.Pie(
        labels=feature_id,
        values=remedy_count
    )

    data = {
        "bar": [bar],
        "pie": [pie],

    }
    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphs_json)


@app.route('/AI/<int:id>', methods=['GET', 'POST'])
def AI(id):

    ####################### Модели ########################
    tone = {'gray': [1, 0, 0, 0], 'pale': [0, 1, 0, 0], 'pink': [0, 0, 1, 0], 'dark': [0, 0, 0, 1]}

    int_fnd = {'strong': 2, 'medium': 1, 'low': 0}
    col_fnd = {'orange': 1, 'sand': 2, 'peach': 3, 'natural': 4, 'ivory': 5, 'chocolate': 6}

    rev_int_fnd = {2:'strong', 1:'medium', 0:'low'}
    rev_col_fnd = {1:'orange', 2:'sand', 3:'peach', 4:'natural', 5:'ivory', 6:'chocolate'}

    train_skin = [
        [56, 4] + tone['gray'],
        [34, 6] + tone['pale'],
        [22, 6] + tone['gray'],
        [20, 9] + tone['dark'],
        [21, 8] + tone['dark'],
        [72, 2] + tone['pale'],
        [42, 5] + tone['pink'],
        [36, 7] + tone['pale'],
        [61, 3] + tone['pink']
    ]

    train_skin_answer_found = [
        [int_fnd['strong']],
        [int_fnd['medium']],
        [int_fnd['medium']],
        [int_fnd['low']],
        [int_fnd['low']],
        [int_fnd['strong']],
        [int_fnd['low']],
        [int_fnd['low']],
        [int_fnd['strong']]
    ]

    train_skin_answer_col = [
        [col_fnd['sand']],
        [col_fnd['peach']],
        [col_fnd['orange']],
        [col_fnd['chocolate']],
        [col_fnd['natural']],
        [col_fnd['natural']],
        [col_fnd['ivory']],
        [col_fnd['peach']],
        [col_fnd['ivory']]
    ]

    rfi = RandomForestClassifier(max_depth=3)
    rfi.fit(train_skin, train_skin_answer_found)

    rfc = RandomForestClassifier(max_depth=3)
    rfc.fit(train_skin, train_skin_answer_col)

    rfi_rfc_query = (
        db.session.query(
            OrmUser.user_age, OrmUser.skin_condition, OrmUser.skin_tone
        ).filter(OrmUser.user_id == id).one()
    )
    vec = list(rfi_rfc_query)
    to_pred = [vec[0], vec[1]] + tone[vec[2]]

    intense_ans = rfi.predict([to_pred])
    color_ans = rfc.predict([to_pred])

    print('Рекомендуемая интенсивность тональной основы: ',rev_int_fnd[intense_ans[0]])
    print('Рекомендуемый оттенок тональной основы: ',rev_col_fnd[color_ans[0]])

    eyh_query = (
        db.session.query(
            OrmUser.hair_color, OrmUser.eye_color
        ).filter(OrmUser.user_id == id).one()
    )
    eye_rec = None
    lip_rec = None

    if eyh_query[0] == 'brunette':
        lip_rec = rnd.choice(['liliac','pink'])
    if eyh_query[0] == 'blonde':
        lip_rec = rnd.choice(['soft-pink','vine'])
    if eyh_query[0] == 'brown':
        lip_rec = rnd.choice(['salmon','vine'])
    else:
        lip_rec ='terracote'


    if eyh_query[1] == 'blue':
        eye_rec = rnd.choice(['violet','bronze'])
    if eyh_query[1] == 'brown':
        eye_rec = rnd.choice(['purple', 'green', 'light-brown'])
    if eyh_query[1] == 'green':
        eye_rec = rnd.choice(['brown, gold', 'light-yellow'])
    else:
        eye_rec ='dark-gray, violet'

    ####################### Корреляция ########################

    cor_query = (
        db.session.query(
            OrmUser.user_age, OrmUser.skin_condition
        ).all()
    )
    x = []
    y = []
    for tup in cor_query:
        x.append(tup[0])
        y.append(tup[1])

    x = np.array(x)
    y = np.array(y)
    corr_m = np.corrcoef(x, y)[0][1]
    print('correlat: ',corr_m)

    model_lin = LinearRegression().fit(x.reshape(-1, 1), y.reshape(-1, 1))
    lcoef = model_lin.coef_
    lint = model_lin.intercept_

    xlin = [0, 100]
    ylin = [lint[0], (lcoef[0]*100 + lint[0])[0]]

    print(xlin, ylin)

    trace_mark = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name='markers'
    )

    trace_line = go.Scatter(
        x=xlin,
        y=ylin,
        mode='lines+markers',
        name='lines+markers'
    )

    # datap = [trace_mark, trace_line]
    data = {
        "markers": [trace_mark],
        "lines": [trace_line]
    }


    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)


    conclusion = ''
    if fabs(corr_m) < 0.35:
        conclusion = 'Взаимосвязь между возрастом и состоянием кожи незначительная'
    if fabs(corr_m) >= 0.35 and fabs(corr_m) < 0.7:
        conclusion = 'Взаимосвязь между возрастом и состоянием кожи основательная'
    if fabs(corr_m) >= 0.7:
        conclusion = 'Возраст сильно влияет на состояние кожи!'
    ####################### Кластеризация ########################

    kmean_query = (
        db.session.query(
            OrmUser.user_age, OrmUser.skin_condition
        ).filter(OrmUser.user_id == id).one()
    )

    model = KMeans(n_clusters=3)
    model.fit(x.reshape(-1, 1), y.reshape(-1, 1))
    predict = model.predict(np.array(list(kmean_query)).reshape(-1,1))

    print('kmean: ',predict)
    # return render_template('success.html')
    return render_template('ai_res.html', intens_osn = rev_int_fnd[intense_ans[0]],
                                        otten_osn = rev_col_fnd[color_ans[0]],
                                        lip_rec = lip_rec,
                                        eye_rec = eye_rec,
                                        corr = round(corr_m, 4),
                                        conclusion = conclusion,
                                        clas = predict,
                                        graphsJSON=graphs_json)

if __name__ == '__main__':
    app.debug = True
    app.run()
