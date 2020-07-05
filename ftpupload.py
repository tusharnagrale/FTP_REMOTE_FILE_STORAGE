"""problem: create a remote storage system

software required:
filezilla client and server

working:
1. create a flask application where user will upload an image by calling an api
   user will also send type of method(normal or tls)
2. if all the conditions are satisfied, store that image in remote storage using ftp protocol
3. return success message to user

note:
the system should support both ftp and ftp tls depending on the user choice."""
# date : july 2 2020

import os
from ftplib import FTP
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from ftplib import FTP_TLS

app = Flask(__name__)

app.secret_key = "secret key"

# to allow only files of the extension
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# file name is fetched and and checked for specific extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# loads form when user request for form
@app.route('/', methods=['GET'])
def upload_form():
    return render_template('file_upload_form.html')


# when the file is uploaded this function is called
@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if filename is empty
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        # if file is available and have extension of mp4, avi, webm is saved in proect directory
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # saving the video file
            file.save(filename)
            flash('File successfully uploaded')
            secure = request.form['secure']
            if secure == "FTP":

                ftp = FTP()

                ftp.connect('localhost', 21)

                status = ftp.login('testuser1', 'testuser')
                print("FTP Connected", status)

                fp = open(filename, 'rb')
                ftp.storbinary('STOR %s' % os.path.basename(filename), fp, 1024)
                return render_template('success.html', name=filename)

            elif secure == "FTP TLS":
                ftps = FTP_TLS('localhost')
                ftps.set_debuglevel(2)
                ftps.login('testuser1', 'testuser')

                ftps.set_pasv(False)
                ftps.prot_p()
                fp = open(filename, 'rb')
                ftps.storbinary('STOR %s' % os.path.basename(filename), fp, 1024)
                return render_template('success.html', name=filename)

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            # return to the same page
            return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)
