from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
# from datetime import datetime
from db_handler import *
from middleware_helpers import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("homepage.html")

@app.route("/dashboard")
def dashboard():
    conn_info = (connection.closed)
    create_urls_table_iff()
    data = fetch_all_db()
    return render_template("dashboard.html", conn_info=conn_info, data=data)

@app.route('/txtsim_dashboard')
def txtsim_dashboard():
    return render_template("txtsim_dashboard.html")

@app.route('/import_from_file', methods=['GET', 'POST'])
def import_from_file():
    if request.method == "POST":
        if request.files['file']:
            f = request.files['file']
            fname = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            urls = formatted(readfile(fname))
            url_dict = track(urls)
            message = insert_urls(url_dict)
            if (message != "if any, Remaining URLS have been added successfully ! "):
                return render_template("errors.html", message=message)
            return redirect(url_for('dashboard'))
        message = "No file choosen"
        return render_template('errors.html', message=message)
    else:
        return render_template("import_from_file.html")


@app.route('/add_urls', methods=['GET', 'POST'])
def add_urls():
    if request.method == "POST":
        urls = request.form['urls']
        urls = formatted(urls)
        url_dict = track(urls)
        message = insert_urls(url_dict)
        if (message != "Remaining URLS have been added successfully ! "):
            return render_template("errors.html", message=message)
        return redirect(url_for('dashboard'))
    else:
        return render_template("add_urls.html")


@app.route('/view', methods=['GET', 'POST'])
def view():
    data = fetch_all_db()
    if request.method == 'POST':
        if request.form.get('delete'):
            url = request.form.get('delete')
            delete_from_db(str(url))
            return redirect(url_for('view'))
        if request.form.get('track'):
            url = request.form.get('track')
            return redirect(url_for('change', url=url))
        return render_template("view.html", data=data)
    else:
        return render_template("view.html", data=data)


@app.route('/changes')
def changes():
    db_data = fetch_all_db()
    db_url_dict = dict()
    urls = []
    print(db_data[0])
    for each in db_data:
        urls.append(each[0])
        db_url_dict[each[0]] = [each[1], each[2],each[3]]
    curr_url_dict = track(urls)
    changed_urls = check_for_changes(db_url_dict, curr_url_dict)
    changed_data = update_db(changed_urls, db_url_dict, curr_url_dict)

    return render_template("changes.html", data=changed_data)


@app.route('/change', methods=['GET', 'POST'])
def change():
    if request.method == "POST":
        urls = formatted(request.form.get('urls'))
        curr_url_dict = track(urls)
        db_data = fetch_all_db()
        db_url_dict = dict()
        for each in db_data:
            db_url_dict[each[0]] = [each[1], each[2]]
        changed_urls = check_for_changes(db_url_dict, curr_url_dict, urls)
        changed_data = update_db(changed_urls, db_url_dict, curr_url_dict)
        return render_template("changes.html", data=changed_data)
    else:
        try:
            return render_template("change.html", url=request.args['url'])
        except Exception as e:
            pass
        return render_template("change.html")


if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = r".\uploads"
    app.config['MAX_CONTENT_PATH'] = 2048  # 2MB
    app.config['DEBUG'] = True
    app.run()
