from flask import Flask, render_template

app = Flask(__name__)

# Endpoint pour la page d'accueil
@app.route('/')
@app.route('/home')
def home():
    return "RAMAFRAXA"

# Endpoint pour la page de portfolio
@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

if __name__ == '__main__':
    app.run(debug=True)
