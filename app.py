import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def mongo_string():
    return os.getenv("MONGODB_URI")

def microblog_db():
    client = MongoClient(mongo_string())
    db = client.microblog
    return db

def create_app():
    app = Flask(__name__)
    app.db = microblog_db()

    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            entry_timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            if (entry_content != "") and (entry_content is not None):
                app.db.entries.insert_one({
                    "content": entry_content,
                    "timestamp": entry_timestamp
                })

        formatted_entries = [
            (
                entry.get("content"),
                (datetime.datetime
                    .strptime(entry.get("timestamp"), "%Y-%m-%d %H:%M:%S")
                    .strftime("%b %d")
                )
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("index.html", entries=formatted_entries)
    
    return app