from flask_app import app
from flask_app.models.camping import Camping
from flask_app.models.user import User
from flask import Flask, render_template, redirect, request, session, flash
import os
import googlemaps
import folium
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from werkzeug.utils import secure_filename


#check if the formau is right
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# @app.route("/tirana")
# def tirana():
#     map = folium.Map(
#         location=[45.52364, -122.34524],
#         tiles='Stamen Toner',
#         zoom_start=13
#     )
#     return map._repr_html_()

@app.route('/tirana')
def tirana():
    # Replace 'your_tile_url' and 'your_attribution' with actual values from your tile provider
    tile_url = 'https://your_tile_url/{z}/{x}/{y}.png'
    attribution = 'Map data &copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors'

    # Create the map with custom tiles and attribution
    map = folium.Map(
        location=[41.3275, 19.8189],  # Replace with desired center coordinates
        zoom_start=13,
        tiles=tile_url,
        attr=attribution
    )

    # Add markers or other elements to the map as needed
    folium.Marker([41.3275, 19.8189], popup='Tirana').add_to(map)

    # Save the map to a temporary file
    map.save('map.html')  # Assuming 'templates' folder exists

    # Render the template with the map
    return render_template('tirana.html')



@app.route("/campings/new")
def addCamping():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("addCamping.html", loggeduser=loggeduser, cities=Camping.get_all_Cityis())


@app.route("/books")
def Books():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("books.html", loggeduser=loggeduser)

@app.route("/about")
def aboutAs():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("about.html", loggeduser=loggeduser)

@app.route("/emergency")
def emergency():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("emergency.html", loggeduser=loggeduser)

@app.route("/contact")
def contact():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("contact.html", loggeduser=loggeduser)


@app.route("/add/camping", methods=["POST"])
def createCamping():
    if "user_id" not in session:
        return redirect("/")
    if not Camping.validate_camping(request.form):
        return redirect(request.referrer)
    if not request.files['image']:
        flash('Show image is required!', 'image')
        return redirect(request.referrer)
    image = request.files['image']
    if not allowed_file(image.filename):
        flash('Image should be in png, jpg, jpeg format!', 'image')
        return redirect(request.referrer)
    if image and  allowed_file(image.filename):
        filename1 = secure_filename(image.filename)
        time = datetime.now().strftime("%d%m%Y%S%f")
        time+= filename1
        filename1 = time
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
    data = {
        "description": request.form["description"],
        "image": filename1,
        "location": request.form["location"],
        'user_id': session['user_id'],
        "city_id": request.form['city']
    }
    Camping.create(data)
    return redirect("/campings")


@app.route("/camping/<int:id>")
def viewCamping(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"camping_id": id, "id": session["user_id"]}
    camping = Camping.get_camping_by_id(data)
    loggeduser = User.get_user_by_id(data)
    usersWhoLiked = Camping.get_users_who_liked(data)
    return render_template("camping.html", camping=camping, loggeduser=loggeduser, usersWhoLiked=usersWhoLiked, numOfLikes=len(Camping.get_users_who_liked(data)))


@app.route("/delete/camping/<int:id>")
def deleteCamping(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"camping_id": id, "id": session["user_id"]}
    camping = Camping.get_camping_by_id(data)
    loggeduser = User.get_user_by_id(data)
    if camping["user_id"] == loggeduser["id"]:
        Camping.delete_all_likes(data)
        Camping.delete_camping(data)
    return redirect("/campings")


@app.route("/camping/edit/<int:id>")
def editCamping(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"camping_id": id, "id": session["user_id"]}
    camping = Camping.get_camping_by_id(data)
    if not camping:
        return redirect('/')
    loggeduser = User.get_user_by_id(data)
    if camping['user_id'] != loggeduser['id']:
        return redirect('/')
    return render_template("editCamping.html", camping=camping, loggeduser=loggeduser)


@app.route("/update/camping/<int:id>", methods=["POST"])
def updateCamping(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"camping_id": id, "id": session["user_id"]}
    camping = Camping.get_camping_by_id(data)
    if not camping:
        return redirect('/')
    loggeduser = User.get_user_by_id(data)
    if camping['user_id'] != loggeduser['id']:
        return redirect('/')
    if (
        len(request.form["description"]) < 1
        or len(request.form["location"]) < 1
    ):
        flash("All fields required", "allRequired")
        return redirect(request.referrer)
    updateData={
        'description': request.form['description'],
        'location': request.form['location'],
        'camping_id':id
    }
    Camping.update_camping(updateData)
    return redirect('/camping/'+ str(id))


@app.route('/like/<int:id>')
def addLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'camping_id': id,
        'id': session['user_id']
    }
    usersWhoLiked = Camping.get_users_who_liked(data)
    if session['user_id'] not in usersWhoLiked:
        Camping.addLike(data)
        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/unlike/<int:id>')
def removeLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'camping_id': id,
        'id': session['user_id']
    }    
    Camping.removeLike(data)
    return redirect(request.referrer)
