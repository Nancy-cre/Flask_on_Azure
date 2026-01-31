from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import app
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('entries/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('ユーザ名が異なります')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('パスワードが異なります')
        else:
            session['logged_in'] = True
            flash('ログインしました')
            return redirect('/')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

@app.route('/azure')
def azure():
    account_url = "https://flaskonazure2026.blob.core.windows.net"
    default_credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_name = "blog2"
    container_client = blob_service_client.create_container(container_name)
    return render_template('/azure.html')