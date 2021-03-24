from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use flask PyMongo to create Mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_DB"
mongo = PyMongo(app)


@app.route("/")
def index():

    # Find a record of the data from mongo 

    mars_data = mongo.db.mars_data.find_one()

    return render_template("index.html", mars_info=mars_data)



@app.route("/scrape")
def scrape():

    mars_data = mongo.db.mars_data
    planet_mars = scrape_mars.scrape()

    # Update the Mongo database
    mongo.db.mars.replace_one({}, planet_mars, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)