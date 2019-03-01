import datetime
import os

from flask import Flask, render_template, redirect, url_for
from forms import ItemForm
from models import Items
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

@app.route("/success")
def success():
    results = []
    resultString = "<strong>Success! You have added the item to the database.</strong><br/><br/>"
    resultString += "(ID, NAME, QUANTITY, DESCRIPTION, DATE_ADDED)<br/><br/>"
    qry = db_session.query(Items)
    results = qry.all()
    for result in results:
        resultString += str(result.id) + " | "+ str(result.name) + " | " + str(result.quantity) + " | "+ str(result.description) + " | "+ str(result.date_added) + "<br/><br/>"
        #print(str(result.id) + " | "+ str(result.name) + " | " + str(result.quantity) + " | "+ str(result.description) + " | "+ str(result.date_added) + "\n")
    
    return resultString[:-10] + "  <= **This is the item your just submitted**"
  

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
