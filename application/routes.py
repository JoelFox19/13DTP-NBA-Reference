from application import app
from flask import render_template
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
   players = do_query ("SELECT information FROM display WHERE teamname=?;",(teamname,),fetchone=False)
   colours = do_query ("SELECT colour FROM display WHERE teamname=?;",(teamname,),fetchone=False)
   return render_template('page.html',title="Team Page", players=players,team_id=team_id,colours=colours,teamimage_id=teamimage_id)

@app.route('/shop')
def shop():
   return render_template('shop.html',title="Shop Page")

@app.route('/tickets')
def tickets():
   return render_template('tickets.html',title="Season Tickets Page")

#pip3 install flask_sqlalchemy