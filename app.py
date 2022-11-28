import random
from datetime import datetime
from flask import render_template

from flask import request
import random
import os
# from flask import Flask, flash, request, redirect, url_for
# from flask import send_from_directory
# from flask import send_file


from flask import Flask,render_template,redirect,request,flash, url_for, abort,send_file,send_from_directory

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my secret key'

def encrypt(file):
    fo = open(file, "rb")
    image=fo.read()
    fo.close()
    image=bytearray(image)
    key=random.randint(0,256)
    for index , value in enumerate(image):
	    image[index] = value^key

    fo = open("enc.jpg","wb")
    imageRes="enc.jpg"
    fo.write(image)
    fo.close()
    return (key,imageRes)

def decrypt(key,file):
    fo = open(file, "rb")
    image=fo.read()
    fo.close()
    image=bytearray(image)
    for index , value in enumerate(image):
	    image[index] = value^key
        
    fo = open("dec.jpg","wb")
    imageRes="dec.jpg"
    fo.write(image)
    fo.close()
    return imageRes




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fileenc')
def fileenc():
    return render_template('fileenc.html')

@app.route('/imageenc')

# def imageenc():
#     return render_template(
#         'imageenc.html'
#         title='Encrypt',
#         year=datetime.now().year,
#         message='Upload the image here')

@app.route('/imageenc')
def imageenc():
    """Renders the about page."""
    return render_template(
        'imageenc.html',
        title='Encrypt',
        year=datetime.now().year,
        message='Upload the image here'
    )

    
        


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Decrypt',
        year=datetime.now().year,
        message='Upload your encrypted image along with the key')
    



@app.route('/contact1', methods = ['POST'])  
def contact1():  
    if request.method == 'POST':  
        global f
        f = request.files['file']  
        f.save(f.filename)  
        text = request.form['key']
        key=int(text)
        image=decrypt(key,f.filename)
        return render_template('contact1.html',
        title='Decrypted',
        year=datetime.now().year,
        message='This is your Decrypted image', name = f.filename) 

@app.route('/img', methods = ['POST'])  
def img():  
    if request.method == 'POST':  
        global f
        f = request.files['file']  
        f.save(f.filename)  
        key,image=encrypt(f.filename)
        return render_template('img.html',
        title='Encrypted',
        year=datetime.now().year,
        message='This is your encrypted image', name = f.filename,keys=key,images=image)

@app.route('/return-file')
def return_file():
    return send_file("../enc.jpg",attachment_filename="enc.jpg")

@app.route('/return-file1')
def return_file1():
    return send_file("../dec.jpg",attachment_filename="dec.jpg")



if __name__ == '__main__':
    app.run(debug=True)

