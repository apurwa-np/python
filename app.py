from flask import Flask

app=Flask(__name__)

@app.route('/')

def webout():

 return '<h1>DevOps is so much fun to learn.<br>All you need is some linux knowledge.<br>This is great !</h1>'

@app.route('/greet')

def weboutg():

 return '<h1>Hey, DevOps is so much fun to learn.<br>All you need is some linux knowledge.<br>This is great !</h1>'

@app.route('/new')

def weboutng():

 return '<h1>New, DevOps is so much fun to learn.<br>All you need is some linux knowledge.<br>This is great !</h1>'

app.run(host='0.0.0.0',port=7000)
