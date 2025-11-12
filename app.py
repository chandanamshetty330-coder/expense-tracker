from flask import Flask, render_template, request
import sqlite3
import datetime

app = Flask(__name__)
conn = sqlite3.connect('expenses.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY, name TEXT, amount REAL, category TEXT, date TEXT)''')
conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        c.execute("INSERT INTO expenses (name, amount, category, date) VALUES (?, ?, ?, ?)",
                  (name, amount, category, date))
        conn.commit()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    return render_template('index.html', expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)

