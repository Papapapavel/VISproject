import datetime
import os 
from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo import MongoClient

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST": 
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            
            app.db.entries.insert_one({"content": entry_content,"date" : formatted_date})

        entries_with_date = []
        for entry in app.db.entries.find({}):
            content = entry.get("content", "-------")
            date = entry.get("date", "")
            if date:
                formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%b %d")
            else:
                formatted_date = ""
            entries_with_date.append((content, date, formatted_date))
            
        return render_template("home.html",entries=entries_with_date)
    return app  

