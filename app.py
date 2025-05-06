from flask import Flask

app=Flask(__name__)

@app.route('/')

def webout():

 return '<h1>DevOps is so much fun to learn.<br>All you need is some linux knowledge</h1>'

app.run(host='0.0.0.0',port=7000)
