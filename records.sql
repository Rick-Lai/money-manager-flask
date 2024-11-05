CREATE TABLE records (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_type TEXT NOT NULL,
    category TEXT NOT NULL,
    amount TEXT NOT NULL ,
    transaction_date DATE NOT NULL,
    notes TEXT
);
