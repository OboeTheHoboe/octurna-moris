from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Events(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     event = db.Column(db.String(200), nullable=False)
     completed = db.Column(db.Integer, default=0)
     date_created = db.Column(db.DateTime, default=datetime.utcnow)

     def __repr__(self):
         return "<Task %r>" % self.id


#db.create_all()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        #gets content of the input with the specified name in the form
        event_event = request.form["event"]
        #create new event object (for our database)
        new_event = Events(event=event_event)

        try:
            #add the new event to the database
            db.session.add(new_event)
            db.session.commit()
            return redirect("/")
        except:
            return "No fue posible agregar el evento"

    else:
        events = Events.query.order_by(Events.date_created).all()
        return render_template("index.html", events=events)



@app.route("/delete/<int:id>")
def delete(id):
    event_to_delete = Events.query.get_or_404(id)

    try:
        db.session.delete(event_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "No se pudo borrar el evento"
    
@app.route("/update/<int:id>", methods=["GET", "POST"])
def info(id):
    event = Events.query.get_or_404(id)

    if request.method == "POST":
        event.event = request.form["event"]
        
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "No se pudo actualizar el evento"
    else:
        return render_template("update.html", event=event)


if __name__ == "__main__":
    app.run(debug=True)