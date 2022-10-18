'''This code was created by Joel Fox in 2022'''



import sqlite3
from flask import render_template, redirect, url_for, request, abort
from application import app

# This is a do_query and it simplifys my code as this query helps my other functions work.
def do_query(query, data=None, fetchone=False):
   ''''query that make functions work'''
   conn = sqlite3.connect('./application/nba.db')
   cur = conn.cursor()
   if data is None: cur.execute(query)
   else: cur.execute(query, data)
   results = cur.fetchone()if fetchone else cur.fetchall()
   conn.close()
   return results


#This query takes everything from the display table and puts it on the 'home.html' page.
@app.route('/')
def home():
   ''''home page'''
   teams = do_query ("SELECT teamname, image FROM display")
   return render_template('home.html',title="Home Page", teams=teams)


#This query shows the team players from the roster
@app.route('/roster')
def player():
   ''''players in the team'''
   player = do_query ("SELECT * FROM Player")
   return render_template('roster.html',title="Roster Page", player=player)


#This query takes all of the different pages and uses
#the display table to show different information on different pages.
@app.route('/page/<string:teamname>')
def pages(teamname):
   ''''information about the team'''
   team_id = do_query("SELECT * FROM display WHERE teamname=?;",(teamname,),fetchone=True)
   teamimage_id = do_query (
      '''SELECT image from display
       WHERE teamname=?;''',(teamname,),fetchone=False)
   players = do_query (
      '''SELECT information, information2, information3,
      information4 FROM display
       WHERE teamname=?;''',(teamname,),fetchone=False)
   colours = do_query (
      '''SELECT colour FROM display
       WHERE teamname=?;''',(teamname,),fetchone=False)
   if team_id is None:
      abort(404)
   return render_template('page.html',title="Team Page",
   players=players,team_id=team_id,colours=colours,
   teamimage_id=teamimage_id)


#This query takes all of the images to display a gallery
#and matches it with the players in each image.
@app.route('/gallery')
def gallery():
   ''''Displays an image gallery'''
   about = do_query ("SELECT image, title FROM picture")
   return render_template('gallery.html',title="Gallery", about=about)


#This query stores the about my website information.
@app.route('/about')
def about():
   ''''about the team page'''
   return render_template('about.html',title="Gallery", about=about)


#This query stores the subsciption list of names and emails in my database.
@app.route('/tickets')
def tickets():
   ''''subscription page'''
   return render_template('tickets.html',title="Season Tickets Page")


#This query is for my subscribe post form.
@app.route('/subscribe',methods=["POST"])
def subscribe():
   ''''subscription form'''
   name = request.form["name"]
   email = request.form["email"]
   news = request.form.get("news")
   conn = sqlite3.connect('./application/nba.db')
   cur = conn.cursor()
   cur.execute("INSERT INTO email (name, email, news) VALUES (?, ?, ?)", (name, email, news))
   conn.commit()
   conn.close()
   return redirect(url_for('tickets')) 


#This query is for my many to many relationship with my player gallery.
@app.route('/playergallery',methods=["POST","GET"])
def playergallery():
   ''''player image sorting for gallery'''
   if request.method=="POST":
      playername = request.form["playername"]
      images = do_query (
         '''SELECT Picture.image FROM player_picture
         JOIN Player ON Player.id = player_picture.player_id
         JOIN Picture ON Picture.id = player_picture.picture_id
         WHERE Player.name=?;''',data=(playername,))
   else:
      images = do_query ("SELECT image FROM Picture")
      players = do_query ("SELECT id, name FROM Player")
   return render_template('gallery.html',title="Gallery Page", images=images, players=players)


#This query lists the players with an integer to match different images.
@app.route('/playerpicture/<int:id>')
def playerpicture(id):
   ''''matching players with images'''
   images = do_query (
      '''SELECT Picture.image FROM player_picture JOIN Player
      ON Player.id = player_picture.player_id JOIN Picture ON
      Picture.id = player_picture.picture_id WHERE Player.id=?;''',data=(id,))
   players = do_query ("SELECT id, name FROM Player")
   return render_template('gallery.html',
                           title="Pictures of Player Page",
                           images=images, players=players)


#This query is for my 404 error page so that users cannot go
#to web pages that do not exist on my website and the 404 page will appear if a user tries to.
@app.errorhandler(404)
def page_not_found(e):
   ''''404 error page'''
   return render_template('404.html'), 404