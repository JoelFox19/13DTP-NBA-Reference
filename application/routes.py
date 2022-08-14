from application import app
from flask import render_template, redirect, url_for, request, abort
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
def roster():
   roster = do_query ("SELECT * FROM Roster")
   return render_template('roster.html',title="Roster Page", roster=roster)

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
   gallery = do_query ("SELECT image, title FROM News")
   return render_template('gallery.html',title="Gallery", gallery=gallery)

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

@app.route('/about')
def about():
   return render_template('about.html',title="About Page")

#This query is for my 404 error page so that users cannot go to web pages that do not exist on my website and the 404 page will appear if a user tries to.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#pip3 install flask_sqlalchemy


