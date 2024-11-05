import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

def db_connect():
    con = sqlite3.connect('records.db')
    return con

@app.route('/')
def welcome():
    return render_template("home.html")

# 獲取全部的資料
@app.route('/record', methods=['GET'])
def get_records():
    with db_connect() as con:
        cur = con.cursor()
        try:
            rows = cur.execute('SELECT * FROM records').fetchall()
        except Exception as e:
            return str(e), 500
    return jsonify(rows)

# 依特定條件排序資料
@app.route('/record/sort_by=<sort_by>', methods=['GET'])
def get_all_records_sorted(sort_by):
    valid_columns = ['transaction_type', 'transaction_date', 'amount', 'category', 'transaction_id']
    if sort_by not in valid_columns:
        return "Invalid colum", 400
    with db_connect() as con:
        cur = con.cursor()
        try:
            rows = cur.execute(f'SELECT * FROM records ORDER BY {sort_by}').fetchall()
        except Exception as e:
            return str(e), 500
    return render_template('response.html', records=rows)

# 僅顯示特定類型的資料，並依指定欄位排序
@app.route('/record/find=<arg1>&<arg2>sort=<arg3>', methods=['GET'])
def get_records_sorted(arg1, arg2, arg3):
    valid_columns = ['transaction_type', 'category']
    if arg1 not in valid_columns:
        return "Invalid colum", 400
    with db_connect() as con:
        cur = con.cursor()
        try:
            rows = cur.execute(f'SELECT * FROM records WHERE {arg1} = ? ORDER BY {arg3}', (arg2,)).fetchall()
            # rows = cur.execute(f'SELECT * FROM records WHERE {arg1} = ? ', (arg2,)).fetchall()
        except Exception as e:
            return str(e), 500
    return render_template('response.html', records=rows)

# 顯示特定日期範圍內的資料
@app.route('/record/date_range=<start_date>&<end_date>', methods=['GET'])
def get_records_date(start_date, end_date):
    with db_connect() as con:
        cur = con.cursor()
        try:
            rows = cur.execute(
                'SELECT * FROM records WHERE transaction_date BETWEEN ? AND ? ORDER BY transaction_date',
                (start_date, end_date)
            ).fetchall()
        except Exception as e:
            return str(e), 500
    return render_template('response.html', records=rows)

# 計算特定日期範圍內的總收支和餘額
@app.route('/record/total_expense=<start_date>&<end_date>', methods=['GET'])
def get_total_expense(start_date, end_date):
    with db_connect() as con:
        cur = con.cursor()
        try:
            total_income = cur.execute(
                'SELECT SUM(amount) FROM records WHERE transaction_type = "收入" AND transaction_date BETWEEN ? AND ?',
                (start_date, end_date)
            ).fetchone()[0]
            total_expense = cur.execute(
                'SELECT SUM(amount) FROM records WHERE transaction_type = "支出" AND transaction_date BETWEEN ? AND ?',
                (start_date, end_date)
            ).fetchone()[0]
        except Exception as e:
            return str(e), 500
    balance = total_income - total_expense
    return jsonify(f'總收入: {total_income} 元', f'總支出: {total_expense} 元', f'餘額: {balance} 元')

# 顯示單筆資料
@app.route('/record/<transaction_id>', methods=['GET'])
def get_record(transaction_id):
    with db_connect() as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM records WHERE transaction_id = ?', (transaction_id,)).fetchone()
        except Exception as e:
            return str(e), 500
    return jsonify(row)

# 新增一筆資料
@app.route('/record/', methods=['POST'])
def add_record():
    with db_connect() as con:
        cur = con.cursor()
        new_record = request.get_json()
        
        transaction_type = new_record['transaction_type']
        category = new_record['category']
        amount = new_record['amount']
        transaction_date = new_record['transaction_date']
        notes = new_record['notes']
        try:
            cur.execute('INSERT INTO records (transaction_type, category, amount, transaction_date, notes) VALUES (?, ?, ?, ?, ?)',
                        (transaction_type, category, amount, transaction_date, notes))
            con.commit()
        except Exception as e:
            return str(e), 500
    return jsonify(new_record)

# 修改單筆資料
@app.route('/record/<transaction_id>', methods=['PUT', 'PATCH'])
def mod_record(transaction_id):
    with db_connect() as con:
        cur = con.cursor()
        # 先取得原本的資料
        record = cur.execute('SELECT * FROM records WHERE transaction_id = ?', (transaction_id,)).fetchone()
        
        transaction_type = record[1]
        category = record[2]
        amount = record[3]
        transaction_date = record[4]
        notes = record[5]

        # 取得要更新的資料並判斷要更新哪些欄位
        update_record = request.get_json()
        if 'transaction_type' in update_record:
            transaction_type = update_record['transaction_type']
        if 'category' in update_record:
            category = update_record['category']
        if 'amount' in update_record:
            amount = update_record['amount']
        if 'transaction_date' in update_record:
            transaction_date = update_record['transaction_date']
        if 'notes' in update_record:
            notes = update_record['notes']
        try:
            cur.execute('UPDATE records SET transaction_type = ?, category = ?, amount = ?, transaction_date = ?, notes = ? WHERE transaction_id = ?',
                        (transaction_type, category, amount, transaction_date, notes, transaction_id))
            con.commit()
        except Exception as e:
            return str(e), 500
    return f'Record {transaction_id} was successfully updated!'


# 刪除單筆資料
@app.route('/record/<transaction_id>', methods=['DELETE'])
def del_record(transaction_id):
    with db_connect() as con:
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM records WHERE transaction_id = ?', (transaction_id,))        
            con.commit()
        except Exception as e:
            return str(e), 500
    return f'Record {transaction_id} was successfully deleted!'

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=7000)