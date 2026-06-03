from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# [VULN] SECRET HARDCODÉ - Gitleaks
# Fake AWS secret key for demonstration purposes
AWS_SECRET_KEY = "AKIAIOSFODNN7E1234BYYMTH2024" 

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
        
        # [VULN] FAILLE SAST - SQL INJECTION - SonarCloud
        # Requête SQL vulnérable par concaténation
        query = f"SELECT * FROM users WHERE name = '{search_query}'"
        
        try:
            c.execute(query)
            results = c.fetchall()
        except sqlite3.Error as e:
            results = [("Erreur base de données", str(e))]
            
        conn.close()
        
    return render_template('index.html', results=results)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
