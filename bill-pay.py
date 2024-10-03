import sqlite3
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            due_date TEXT,
            amount_due REAL,
            importance INTEGER,
            balance REAL,
            payment_history TEXT
        )
    ''')
    conn.commit()
    return conn

class Bill:
    def __init__(self, name, due_date, amount_due, importance, balance=0, payment_history=None, bill_id=None):
        self.id = bill_id
        self.name = name
        self.due_date = datetime.strptime(due_date, '%Y-%m-%d')
        self.amount_due = amount_due
        self.importance = importance
        self.balance = balance
        self.payment_history = payment_history or []

    def add_payment(self, amount, date):
        payment_date = datetime.strptime(date, '%Y-%m-%d')
        self.payment_history.append((amount, payment_date))
        self.balance -= amount
        if self.balance < 0:
            self.balance = 0

    def update_amount_due(self):
        if datetime.now() > self.due_date and self.balance > 0:
            self.amount_due += self.balance
            self.balance = 0

    def __str__(self):
        return f"{self.name}: Due on {self.due_date.date()}, Amount Due: {self.amount_due}, Balance: {self.balance}, Importance: {self.importance}"

class BudgetManager:
    def __init__(self, conn, pay_dates):
        self.conn = conn
        self.bills = self.load_bills()
        self.pay_dates = [datetime.strptime(pay_date, '%Y-%m-%d') for pay_date in pay_dates]
        self.end_balance = 0

    def load_bills(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM bills")
        rows = cursor.fetchall()
        bills = []
        for row in rows:
            bill = Bill(
                name=row[1],
                due_date=row[2],
                amount_due=row[3],
                importance=row[4],
                balance=row[5],
                payment_history=eval(row[6]) if row[6] else [],
                bill_id=row[0]
            )
            bills.append(bill)
        return bills

    def add_bill(self, bill):
        self.bills.append(bill)
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO bills (name, due_date, amount_due, importance, balance, payment_history)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (bill.name, bill.due_date.strftime('%Y-%m-%d'), bill.amount_due, bill.importance, bill.balance, str(bill.payment_history)))
        self.conn.commit()
        bill.id = cursor.lastrowid

    def pay_bills(self, pay_amount):
        self.bills.sort(key=lambda x: x.importance)
        remaining_pay = pay_amount
        for bill in self.bills:
            if remaining_pay >= bill.amount_due:
                remaining_pay -= bill.amount_due
                bill.add_payment(bill.amount_due, str(datetime.now().date()))
            else:
                bill.add_payment(remaining_pay, str(datetime.now().date()))
                remaining_pay = 0
            self.update_bill_in_db(bill)
            print(f"Paid: {bill.name}, Remaining Pay: {remaining_pay}")
        self.end_balance = remaining_pay
        print(f"End Balance after payments: {self.end_balance}")

    def update_bills(self):
        for bill in self.bills:
            bill.update_amount_due()
            self.update_bill_in_db(bill)

    def update_bill_in_db(self, bill):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE bills
            SET amount_due = ?, balance = ?, payment_history = ?
            WHERE id = ?
        ''', (bill.amount_due, bill.balance, str(bill.payment_history), bill.id))
        self.conn.commit()

    def __str__(self):
        return "\n".join(str(bill) for bill in self.bills)

# Example Usage:
# Initialize the database
conn = init_db()

# Enter pay dates
pay_dates = ['2024-10-01', '2024-10-15', '2024-10-31']

# Create Budget Manager
budget_manager = BudgetManager(conn, pay_dates)

# Add bills
bill1 = Bill(name='Rent', due_date='2024-10-05', amount_due=1200, importance=1)
bill2 = Bill(name='Electricity', due_date='2024-10-10', amount_due=100, importance=2)
bill3 = Bill(name='Internet', due_date='2024-10-20', amount_due=60, importance=3)

# Add bills to the budget manager
budget_manager.add_bill(bill1)
budget_manager.add_bill(bill2)
budget_manager.add_bill(bill3)

# Show bills before payments
print("Bills before payments:")
print(budget_manager)

# Pay bills with a $1500 paycheck
budget_manager.pay_bills(1500)

# Update bills for next pay period (rollover past due amounts)
budget_manager.update_bills()

# Show bills after payments and update
print("\nBills after payments:")
print(budget_manager)

# Close the database connection when done
conn.close()
