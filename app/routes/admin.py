import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from extensions import db

from app.models.models import (
    Course,
    Lecture
)

admin = Blueprint("admin", __name__)


ALLOWED_IMAGE_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg"
}

ALLOWED_VIDEO_EXTENSIONS = {
    "mp4",
    "mov",
    "avi"
}


def allowed_file(filename, allowed_extensions):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in allowed_extensions
    )


@admin.route("/admin")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        return "Access Denied"

    return render_template("admin.html")


@admin.route("/create-course", methods=["POST"])
@login_required
def create_course():

    if current_user.role != "admin":
        return "Access Denied"

    title = request.form.get("title")

    description = request.form.get("description")

    price = request.form.get("price")

    image = request.files.get("image")

    filename = None

    if image and allowed_file(
        image.filename,
        ALLOWED_IMAGE_EXTENSIONS
    ):

        filename = secure_filename(image.filename)

        image_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "course_images",
            filename
        )

        image.save(image_path)

    course = Course(
        title=title,
        description=description,
        price=price,
        image=filename
    )

    db.session.add(course)

    db.session.commit()

    return redirect(url_for("courses.courses_page"))


@admin.route("/create-lecture", methods=["POST"])
@login_required
def create_lecture():

    if current_user.role != "admin":
        return "Access Denied"

    title = request.form.get("title")

    course_id = request.form.get("course_id")

    video = request.files.get("video")

    filename = None

    if video and allowed_file(
        video.filename,
        ALLOWED_VIDEO_EXTENSIONS
    ):

        filename = secure_filename(video.filename)

        video_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "lecture_videos",
            filename
        )

        video.save(video_path)

    lecture = Lecture(
        title=title,
        video_url=filename,
        course_id=course_id
    )

    db.session.add(lecture)

    db.session.commit()

    return redirect(url_for("admin.admin_dashboard"))