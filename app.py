from flask import Flask,render_template,request,redirect,url_for
app=Flask(__name__)

#endpoint pour la page d'accueil
@app.route('/')
@app.route('/home')
def home():
    return "RAMAFRAXA"

if __name__=='__main__':
    app.run(debug=True)