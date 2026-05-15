from flask import Flask, render_template,request,redirect,url_for, send_from_directory
from config import Config
from extensions import db,login_manager
from models.models import User, Course, Lecture, Purchase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/courses")
def courses():
    all_courses=Course.query.all()
    return render_template(
        "courses.html",
        courses=all_courses
    )


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")

        email=request.form.get("email")

        password=request.form.get("password")

        hashed_password=generate_password_hash(password)

        user= User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login(): 
    if request.method=="POST":
        
        email=request.form.get("email")

        password=request.form.get("password")
        
        user=User.query.filter_by(email=email).first()
        
        
        if user and check_password_hash(user.password, password):
            
            login_user(user)

            return redirect(url_for("dashboard"))
            
    return render_template("login.html")
    
@app.route("/dashboard")
@login_required
def dashboard():
    purchases = Purchase.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "dashboard.html",
        purchases=purchases
    )

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("home"))

@app.route("/admin")
@login_required
def admin():
    
    if current_user.role!="admin":
        return "Access Denied"
    return render_template("admin.html")

@app.route("/create-course",methods=["POST"])
@login_required
def create_course():
    if current_user.role !="admin":
        return "Access Denied"
    title=request.form.get("title")
    description=request.form.get("description")
    price=request.form.get("price")
    image=request.files.get("image")
    filename=None

    if image and allowed_file(
        image.filename,
        ALLOWED_IMAGE_EXTENSIONS
    ):
        filename=secure_filename(image.filename)
        image_path=os.path.join(
            app.config["UPLOAD_FOLDER"],
            "course_images",
            filename
        )

        image.save(image_path)

    course=Course(
        title=title,
        description=description,
        price=price
    )
    db.session.add(course)
    db.session.commit()
    return redirect(url_for("courses"))

@app.route("/course/<int:course_id>")
def course_details(course_id):
    course=Course.query.get_or_404(course_id)
    return render_template(
        "course_details.html",
        course=course
    )

@app.route("/lecture/<int:lecture_id>")
@login_required
def watch_lecture(lecture_id):

    lecture = Lecture.query.get_or_404(lecture_id)
    purchase = Purchase.query.filter_by(
        user_id=current_user.id,
        course_id=lecture.course_id
    ).first()
    if not purchase:
        return "You must purchase this course first."

    return render_template(
        "watch_lecture.html",
        lecture=lecture
    )

@app.route("/buy-course/<int:course_id>")
@login_required
def buy_course(course_id):

    existing_purchase=Purchase.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()

    if existing_purchase:
        return "You already own this course."
    
    purchase=Purchase(
        user_id=current_user.id,
        course_id=course_id
    )

    db.session.add(purchase)
    db.session.commit()

    return redirect(url_for("dashboard"))

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):

    return send_from_directory(
        "uploads",
        filename
    )

@app.route("/create-lecture", methods=["POST"])
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
            app.config["UPLOAD_FOLDER"],
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

    return redirect(url_for("admin"))

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}

ALLOWED_VIDEO_EXTENSIONS = {"mp4", "mov", "avi"}


def allowed_file(filename, allowed_extensions):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in allowed_extensions
    )

if __name__ == "__main__":
    app.run(debug=True)