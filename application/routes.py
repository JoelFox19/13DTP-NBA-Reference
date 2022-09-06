from application import app
from flask import render_template, redirect, url_for, request, abort, current_app, g
import sqlite3


def do_query(query, data=None, fetchone=False):
   conn = sqlite3.connect('./application/nba.db')
   cur = conn.cursor()
   if data is None:
      cur.execute(query)
   else:
      cur.execute(query, data)
   results = cur.fetchone()if fetchone else cur.fetchall()
   conn.close()
   return results

@app.route('/')
def home():
   teams = do_query ("SELECT teamname, image FROM display")
   return render_template('home.html',title="Home Page", teams=teams)

@app.route('/roster')
def player():
   player = do_query ("SELECT * FROM Player")
   return render_template('roster.html',title="Roster Page", player=player)

@app.route('/page/<string:teamname>')
def pages(teamname):
   team_id = do_query ("SELECT * FROM display WHERE teamname=?;",(teamname,),fetchone=True)
   teamimage_id = do_query ("SELECT image from display WHERE teamname=?;",(teamname,),fetchone=False)
   players = do_query ("SELECT information, information2, information3, information4 FROM display WHERE teamname=?;",(teamname,),fetchone=False)
   colours = do_query ("SELECT colour FROM display WHERE teamname=?;",(teamname,),fetchone=False)
   if team_id is None:
      abort(404)
   return render_template('page.html',title="Team Page", players=players,team_id=team_id,colours=colours,teamimage_id=teamimage_id)

@app.route('/gallery')
def gallery():
   about = do_query ("SELECT image, title FROM picture")
   #join_image = do_query ("SELECT Player.name FROM player_picture JOIN Player ON Player.id = player_picture.player_id WHERE player_picture.picture_id=?;")
   return render_template('gallery.html',title="Gallery", about=about)

@app.route('/about')
def about():
   #join_image = do_query ("SELECT Player.name FROM player_picture JOIN Player ON Player.id = player_picture.player_id WHERE player_picture.picture_id=?;")
   return render_template('about.html',title="Gallery", about=about)

@app.route('/tickets')
def tickets():
   return render_template('tickets.html',title="Season Tickets Page")

@app.route('/subscribe',methods=["POST"])
def subscribe():
   name = request.form["name"]
   email = request.form["email"]
   news = request.form.get("news")
   conn = sqlite3.connect('./application/nba.db')
   cur = conn.cursor()
   cur.execute("INSERT INTO email (name, email, news) VALUES (?, ?, ?)", (name, email, news))
   conn.commit()
   conn.close()
   return redirect(url_for('tickets')) 

@app.route('/playergallery',methods=["POST","GET"])
def playergallery():
   if request.method=="POST":
      playername = request.form["playername"]
      images = do_query ("SELECT Picture.image FROM player_picture JOIN Player ON Player.id = player_picture.player_id JOIN Picture ON Picture.id = player_picture.picture_id WHERE Player.name=?;",data=(playername,))
   else:
      images = do_query ("SELECT image FROM Picture")
      players = do_query ("SELECT id, name FROM Player")
   return render_template('gallery.html',title="Gallery Page", images=images, players=players)

@app.route('/playerpicture/<int:id>')
def playerpicture(id):
   images = do_query ("SELECT Picture.image FROM player_picture JOIN Player ON Player.id = player_picture.player_id JOIN Picture ON Picture.id = player_picture.picture_id WHERE Player.id=?;",data=(id,))
   players = do_query ("SELECT id, name FROM Player")
   return render_template('gallery.html', title="Pictures of Player Page", images=images, players=players)

#This query is for my 404 error page so that users cannot go to web pages that do not exist on my website and the 404 page will appear if a user tries to.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#pip3 install flask_sqlalchemy


