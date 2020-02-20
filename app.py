from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", listings=mars_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_results = scrape_mars.scrape()
    print(mars_results)
    mars_data.update({}, mars_results, upsert=True)
    return redirect("/", code=302)

# below runs the code if this is the file that was run rather than it was imported
if __name__ == "__main__":
    app.run(debug=True)

