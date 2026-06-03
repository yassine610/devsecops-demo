import os
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# [FIX] SECRET SÉCURISÉ - Gitleaks passera au vert
# On n'écrit plus le secret dans le code. On le lit depuis l'environnement.
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "Secret-Non-Defini")

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')
    c.execute('''INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Alice'), (2, 'Bob')''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        search_query = request.form.get('query', '')
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # [FIX] FAILLE SAST CORRIGÉE - SonarCloud passera au vert
        # Utilisation d'une requête "paramétrée" (le '?' protège contre l'injection SQL)
        query = "SELECT * FROM users WHERE name = ?"
        
        try:
            # On passe search_query comme un paramètre sécurisé
            c.execute(query, (search_query,))
            results = c.fetchall()
        except sqlite3.Error as e:
            results = [("Erreur base de données", str(e))]
            
        conn.close()
        
    return render_template('index.html', results=results)

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000)
