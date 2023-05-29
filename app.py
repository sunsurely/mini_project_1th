from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from bson import ObjectId

from pymongo import MongoClient
client = MongoClient('')
db = client.dbsparta
 
@app.route('/')
def home():
   return render_template('index.html')



@app.route("/wishlist", methods=["POST"])                  #최초 상품글 작성시 DB에 쌓을 것들
def wishlist_post():                                       
    name_receive = request.form['name_give']
    description_receive = request.form['description_give']
    nickname_receive = request.form['nickname_give']
    price_receive = request.form['price_give']
    url_receive = request.form['url_give']
    category_receive = request.form['category_give']
          
    doc={
        'name': name_receive,
        'description':description_receive,
        'nickname': nickname_receive,
        'price': price_receive,
        'url': url_receive,
        'category': category_receive                          
    }
    db.wish.insert_one(doc)
    return jsonify({'msg': '등록완료'})
  
@app.route('/wishupdate', methods=['Put'])
def update_product():
    name_receive = request.form['name_give']
    description_receive = request.form['description_give']
    nickname_receive = request.form['nickname_give']
    price_receive = request.form['price_give']
    url_receive = request.form['url_give']
    category_receive = request.form['category_give']
    id_receive = request.form['id_give']
    doc={
        'name': name_receive,
        'description':description_receive,
        'nickname': nickname_receive,
        'price': price_receive,
        'url': url_receive,
        'category': category_receive                          
    }
    db.wish.update_one( {'_id':ObjectId(id_receive)}, {'$set': doc})
    return jsonify({'msg': '등록완료'})

@app.route('/deletewish', methods=['DELETE'])
def delete_item():
    id_receive = request.form['id_give']
    id= ObjectId(id_receive)
    db.wish.delete_one({'_id': id})
    return {'msg': '삭제되었습니다.'}




@app.route("/wishlist", methods=["GET"])
def wishlist_get():
    rows = list(db.wish.find({},{"_id": True, "url": True, "name": True, "nickname": True, "price": True, "description": True, "category": True}))
    for row in rows:
        row["_id"] = str(row["_id"])
    return jsonify({"products": rows})


if __name__ == '__main__':
       app.run('0.0.0.0',port=5000,debug=True)