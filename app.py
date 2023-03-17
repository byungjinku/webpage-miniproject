from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import bcrypt

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.alhagr5.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    count_list = db.vive02.find_one({'name': 'comment'})
    count = count_list['num'] + 1
    db.vive02.update_one({'name': 'comment'}, {'$inc': {'num': 1}})

    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    pw_receive = request.form['pw_give']

    if (name_receive == "") and (comment_receive == "") and (pw_receive == ""):
        return jsonify({'msg': '저장 실패!'})
    else:
        doc = {
            'name': name_receive,
            'comment': comment_receive,
            'pw': pw_receive,
            'num': count
        }

    hashed_password = bcrypt.hashpw(doc["pw"].encode('UTF-8'), bcrypt.gensalt())
    decoded_password = hashed_password.decode("utf-8")

    doc["pw"] = decoded_password

    db.vive01.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_comments = list(db.vive01.find({}, {'_id': False, 'pw': False}))
    return jsonify({'result': all_comments})


@app.route("/like", methods=["POST"])
def like_post():
    like_receive = request.form['like_give']
    print(like_receive)

    doc1 = {
        'name': 'not_vive',
        'like': 1
    }

    db.vive02.update_one({'name': 'vive'}, {'$inc': {'like': 1}})

    return jsonify({'msg': '좋아요 완료!'})


@app.route("/like", methods=["GET"])
def like_get():
    likes = list(db.vive02.find({}, {'_id': False}))
    return jsonify({'likecnt': likes})


@app.route("/delete", methods=["POST"])
def delete_post():
    num_receive = request.form['num_give']
    pw_receive = request.form['pw_give']

    num = int(num_receive)

    delete_comment = db.vive01.find_one({"num": num})['pw']

    input_pw = pw_receive.encode('utf-8')
    db_pw = delete_comment.encode('utf-8')
    check_pw = bcrypt.checkpw(input_pw,db_pw)

    if (check_pw == True) :
        db.vive01.delete_one({'num': num})
        return jsonify({'msg': '삭제 완료!'})
    else:
        return jsonify({'msg': '비밀번호를 확인해주세요!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
