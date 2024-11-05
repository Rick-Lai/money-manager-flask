# 使用官方 Python 3.11 映像
FROM python:3.11.7

# 設定工作目錄
WORKDIR /app

# 複製必要的檔案到映像
COPY ./app /app
COPY requirements.txt /app/requirements.txt
COPY new_db.py /app/new_db.py
COPY records.sql /app/records.sql
COPY transaction_records_1000.csv /app/transaction_records_1000.csv

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt
RUN python new_db.py

# 暴露應用埠 (例如 8000)
EXPOSE 7000

# 啟動  應用
CMD ["python", "app.py"]