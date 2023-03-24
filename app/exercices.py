from flask import Blueprint, request, render_template, redirect, url_for, request, flash
from . import db
from .models.Category import Category
from .models.Exercise import Exercise

from sqlalchemy.sql.expression import func
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired


exercises = Blueprint("exercises", __name__)


class ExerciseForm(FlaskForm):

    name = StringField("name", validators=[DataRequired()])
    description = TextAreaField("description")
    category = SelectField(validators=[DataRequired()])


@exercises.route("/create", methods=["GET", "POST"])
def create_exercise():

    form = ExerciseForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        check_exo_exits = Exercise.query.filter_by(name=form.name.data).first()

        if check_exo_exits == None:
            exo = Exercise(
                name=form.name.data, description=form.description.data, category=form.category.data)

            db.session.add(exo)
            db.session.commit()
            flash("Exo created !")
            return redirect("/exos/all")

        else:
            flash("Exo name alreadry exist !", category="error")

    return render_template("formExo.html", form=form)



@exercises.route("/all", methods=["GET"])
def get_all_exos():

    exos = Exercise.query.all()
    return render_template("exos.html", exos=exos)