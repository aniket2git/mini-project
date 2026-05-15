from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db

from app.models.models import (
    Course,
    Lecture,
    Purchase
)

courses = Blueprint("courses", __name__)


@courses.route("/courses")
def courses_page():

    all_courses = Course.query.all()

    return render_template(
        "courses.html",
        courses=all_courses
    )


@courses.route("/course/<int:course_id>")
def course_details(course_id):

    course = Course.query.get_or_404(course_id)

    return render_template(
        "course_details.html",
        course=course
    )


@courses.route("/buy-course/<int:course_id>")
@login_required
def buy_course(course_id):

    existing_purchase = Purchase.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()

    if existing_purchase:
        return "You already own this course."

    purchase = Purchase(
        user_id=current_user.id,
        course_id=course_id
    )

    db.session.add(purchase)

    db.session.commit()

    return redirect(
        url_for("courses.dashboard")
    )


@courses.route("/dashboard")
@login_required
def dashboard():

    purchases = Purchase.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "dashboard.html",
        purchases=purchases
    )


@courses.route("/lecture/<int:lecture_id>")
@login_required
def watch_lecture(lecture_id):

    lecture = Lecture.query.get_or_404(
        lecture_id
    )

    purchase = Purchase.query.filter_by(
        user_id=current_user.id,
        course_id=lecture.course_id
    ).first()

    if not purchase:
        return "Purchase this course first."

    return render_template(
        "watch_lecture.html",
        lecture=lecture
    )