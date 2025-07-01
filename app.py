
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

DATA_FILE = 'transactions.csv'
CATEGORIES = ['Food', 'Rent', 'Utilities', 'Salary', 'Entertainment', 'Travel', 'Other']

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df
    else:
        return pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount', 'Note'])


# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Add new transaction
def add_transaction(date, t_type, category, amount, note):
    df = load_data()
    new_entry = pd.DataFrame({
        'Date': [date],
        'Type': [t_type],
        'Category': [category],
        'Amount': [amount],
        'Note': [note]
    })
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    st.success("Transaction added successfully!")

# Streamlit UI
st.title("💰 Budget Tracking & Financial Dashboard")

menu = st.sidebar.selectbox("Menu", ["Add Transaction", "View Dashboard", "Raw Data"])

if menu == "Add Transaction":
    st.header("➕ Add New Transaction")
    date = st.date_input("Date", datetime.today())
    t_type = st.selectbox("Type", ["Income", "Expense"])
    category = st.selectbox("Category", CATEGORIES)
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    note = st.text_input("Note (optional)")

    if st.button("Add"):
        add_transaction(date, t_type, category, amount, note)

elif menu == "View Dashboard":
    st.header("📊 Dashboard Overview")
    df = load_data()
    if df.empty:
        st.warning("No data available. Add some transactions first.")
    else:
        income = df[df['Type'] == 'Income']['Amount'].sum()
        expense = df[df['Type'] == 'Expense']['Amount'].sum()
        balance = income - expense

        st.metric("Total Income", f"₹{income:,.2f}")
        st.metric("Total Expense", f"₹{expense:,.2f}")
        st.metric("Net Balance", f"₹{balance:,.2f}")

        cat_exp = df[df['Type'] == 'Expense'].groupby('Category')['Amount'].sum().reset_index()
        if not cat_exp.empty:
            fig_pie = px.pie(cat_exp, values='Amount', names='Category', title='Expenses by Category')
            st.plotly_chart(fig_pie)

        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        monthly = df.groupby(['Month', 'Type'])['Amount'].sum().reset_index()
        fig_line = px.line(monthly, x='Month', y='Amount', color='Type', markers=True, title='Monthly Trend')
        st.plotly_chart(fig_line)

elif menu == "Raw Data":
    st.header("📄 All Transactions")
    df = load_data()
    st.dataframe(df)
