import sqlite3
import requests
import json
from better_profanity import profanity
from flask import Flask, request


app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def check_language(text):
    return profanity.contains_profanity(text)


@app.route('/sentences', methods=['POST'])
def sentences():
    has_foul_language = False
    if request.method == 'POST':
        fragment = request.form.get('fragment', None)
        if fragment:
            has_foul_language = check_language(fragment)
        else:
            json.dumps({'success': False}), 400
    return json.dumps({'hasFoulLanguage': has_foul_language}), 200


def moderator(comments):
    moderated, foul_lang = None, False
    for each in comments.split('\n'):
        res = requests.post("http://localhost:5000/sentences", data={'fragment': each})
        if res.get('status_code', None) in [503]:
            moderated = None
            break
        elif res.get('status_code', None) == 200:
            moderated = True
            foul_lang = res['hasFoulLanguage']
            if foul_lang:
                break
    return moderated, foul_lang


@app.route('/post', methods=['POST'])
def posts():
    if request.method == 'POST':
        comments = request.form.get('paragraphs', None)
        if not comments:
            return json.dumps({'success': False}), 400
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO posts (comments) VALUES (?)',
                         (comments,))
            conn.commit()
            # for each sentence -> make async call to check and update moderate sentences
            moderated = None
            moderated, foul_lang = moderator(comments)
            if moderated:
                # update the full comment as foul and set as moderated
                cursor.execute('''UPDATE posts set is_foul=?, moderated=1 WHERE id = ?''',
                        (foul_lang, cursor.lastrowid))
            conn.commit()
            conn.close()
            return json.dumps({'success': True}), 201
    return json.dumps({'success': False}), 400


def daily_moderator():
    # script that can be scheduled to update moderator for text which are missed
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * from posts WHERE moderated=0')
    unmoderated_data = cursor.fetchall()
    for each in unmoderated_data:
        moderated, foul_lang = moderator(each['comments'])
        if moderated:
            cursor.execute('''UPDATE posts set is_foul=?, moderated=1 WHERE id = ?''',
                        (foul_lang, each['id']))
    conn.commit()
    conn.close()
