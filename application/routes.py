from re import T
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

@app.route('/gsw_team/<int:id>')
def gsw_team():
   players = do_query ("SELECT * from Players WHERE id=?;",(id,),fetchone=True)
   return render_template('gsw.html',title="GSW Page", players=players)
#pip3 install flask_sqlalchemy