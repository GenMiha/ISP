from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
database = SQLAlchemy(app)
#database.create_all()
migration = Migrate(app, database)
#database.create_all()

#if __name__ == '__main__':
    #database.create_all()
    #app.run()