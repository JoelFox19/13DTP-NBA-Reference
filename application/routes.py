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
   teams = do_query ("SELECT teamname, image FROM teams")
   return render_template('home.html',title="Home Page", teams=teams)

@app.route('/teams/<string:teamname>')
def teams(teamname):
   team_id = do_query ("SELECT * from Teams WHERE teamname=?;",(teamname,),fetchone=True)
   players = do_query ("SELECT * FROM Players WHERE team_id=?;",(team_id[0],),fetchone=False)
   colours = do_query ("SELECT colour FROM teams")
   return render_template('team.html',title="Team Page", players=players,team_id=team_id,colours=colours)


#pip3 install flask_sqlalchemy