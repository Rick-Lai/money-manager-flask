# 使用官方 Python 3.11 映像
FROM python:3.11.7-slim

# 設定工作目錄
WORKDIR /app

# 複製必要的檔案到映像
COPY app app/
COPY requirements.txt new_db.py records.sql transaction_records_1000.csv /app/

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt
RUN python new_db.py

# 暴露應用埠 (例如 8000)
EXPOSE 7000

# 啟動  應用
CMD ["python", "app/app.py"]