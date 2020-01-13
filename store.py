import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = (os.getcwd() + "/file/")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    
    filedir = os.getcwd()
    list_dir = os.listdir(app.config['UPLOAD_FOLDER'])
    list_dir.sort()
    html_front = '''
    <!doctype html>
    <html>
    <head>
    <title>Upload</title>
    </head>
    <body>
    <h1>Upload Your Text File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    for file_name in list_dir:
        html_front = html_front + '''<p><a href="''' +'/file/' + file_name + '''/view''' +'''">''' + file_name + '''</a></p>'''
    html_front = html_front + '''</body></html>'''
    return html_front

@app.route('/file/<filedir>/view')
def view(filedir):
    middle_html = '<h4>'+filedir+'</h4>\n'
    f = open(os.getcwd()+'/file/'+filedir,'r')
    line = f.readline()
    while line:
        if line == '\n':
            middle_html = middle_html+'<br></br>\n'
        else:
            middle_html = middle_html+'<p>'+line+'</p>\n'
        line = f.readline()
    f.close()
    return middle_html


if __name__ == '__main__':
    app.run()
