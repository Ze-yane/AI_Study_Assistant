import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import io


class BudgetTracker:
    def __init__(self, db_path="budget.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                amount REAL,
                note TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def add_transaction(self, date, category, amount, note):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO transactions (date, category, amount, note) VALUES (?, ?, ?, ?)",
            (date, category, amount, note),
        )
        conn.commit()
        conn.close()

    def list_transactions(self, limit=100):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id, date, category, amount, note FROM transactions ORDER BY date DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        return rows

    def delete_transaction(self, tx_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM transactions WHERE id=?", (tx_id,))
        conn.commit()
        conn.close()

    def get_dataframe(self):
        """Get all transactions as pandas DataFrame"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM transactions ORDER BY date DESC", conn)
        conn.close()
        return df

    def summary(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT SUM(amount), category FROM transactions GROUP BY category")
        data = c.fetchall()
        conn.close()
        total = sum(row[0] for row in data) if data else 0.0
        return total, data

    def import_csv(self, csv_file):
        """Import transactions from CSV"""
        try:
            df = pd.read_csv(csv_file)
            count = 0
            for _, row in df.iterrows():
                try:
                    self.add_transaction(
                        str(row.get('date', datetime.today().isoformat())),
                        str(row.get('category', 'General')),
                        float(row.get('amount', 0.0)),
                        str(row.get('note', ''))
                    )
                    count += 1
                except Exception as e:
                    st.warning(f"Skipped row: {e}")
            return count
        except Exception as e:
            st.error(f"CSV import error: {e}")
            return 0

    def export_csv(self):
        """Export transactions to CSV bytes"""
        try:
            df = self.get_dataframe()
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            return csv_buffer.getvalue().encode('utf-8')
        except Exception as e:
            st.error(f"Export error: {e}")
            return None

    def ui(self):
        st.subheader("💰 Add Transaction")
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("📅 Date", value=datetime.today())
        with col2:
            category = st.selectbox("📌 Category", ["🍔 Food", "🚗 Transport", "🎬 Entertainment", "⚡ Utilities", "❤️ Health", "🏠 Rent", "📚 Education", "🛍️ Shopping", "💼 Work", "❓ Other"], help="Select a category for tracking")
        with col3:
            amount = st.number_input("💵 Amount ($)", format="%.2f", value=0.00, min_value=0.0, step=0.01)
        
        note = st.text_input("📝 Note (optional)", placeholder="E.g., Grocery store, Gas, Movie tickets...")

        if st.button("✅ Add Transaction", use_container_width=True):
            if amount > 0:
                # Remove emoji prefix for storage
                clean_category = category.split(' ', 1)[1] if ' ' in category else category
                self.add_transaction(date.isoformat(), clean_category, amount, note)
                st.success("✓ Transaction added!")
                st.rerun()
            else:
                st.error("Amount must be greater than 0")

        st.divider()
        st.subheader("📊 Import / Export")
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_csv = st.file_uploader("Upload CSV to import", type=['csv'])
            if uploaded_csv and st.button("📥 Import CSV"):
                count = self.import_csv(uploaded_csv)
                st.success(f"✓ Imported {count} transactions!")
                st.rerun()
        
        with col2:
            csv_data = self.export_csv()
            if csv_data:
                st.download_button(
                    label="📥 Export as CSV",
                    data=csv_data,
                    file_name=f"transactions_{datetime.today().date()}.csv",
                    mime='text/csv'
                )

        st.divider()
        st.subheader("📋 All Transactions")
        transactions = self.list_transactions(200)
        if transactions:
            for tx_id, date, category, amount, note in transactions:
                col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1.5, 0.8])
                with col1:
                    st.caption(f"#{tx_id}")
                with col2:
                    st.write(date)
                with col3:
                    st.write(category)
                with col4:
                    st.write(f"${amount:.2f}")
                with col5:
                    if st.button("🗑️", key=f"del_{tx_id}", use_container_width=True):
                        self.delete_transaction(tx_id)
                        st.rerun()
        else:
            st.info("No transactions yet. Add one above!")

        st.divider()
        st.subheader("💹 Summary & Charts")
        total, by_category = self.summary()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Total Spent", f"${total:.2f}")
        
        with col2:
            if by_category:
                st.metric("📊 Categories", len(by_category))
        
        if by_category:
            # Create pie chart
            categories = [cat for _, cat in by_category]
            amounts = [amt for amt, _ in by_category]
            
            fig, ax = plt.subplots(figsize=(8, 5))
            colors = plt.cm.Set3(range(len(categories)))
            wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
            ax.set_title('Spending by Category', fontsize=14, fontweight='bold')
            
            # Make percentage text readable
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontsize(10)
            
            st.pyplot(fig)
            
            # Category breakdown table
            st.write("**Category Breakdown:**")
            for amount, category in by_category:
                st.write(f"  • {category}: **${amount:.2f}**")
        
        # Advanced Analytics
        st.divider()
        st.subheader("📈 Advanced Analytics")
        
        df = self.get_dataframe()
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Daily Spending Trend**")
                daily = df.groupby('date')['amount'].sum().sort_index()
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(daily.index, daily.values, marker='o', linewidth=2, markersize=6, color='#667eea')
                ax.fill_between(daily.index, daily.values, alpha=0.3, color='#667eea')
                ax.set_xlabel('Date')
                ax.set_ylabel('Amount ($)')
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            
            with col2:
                st.write("**Monthly Spending**")
                df['month'] = df['date'].dt.to_period('M')
                monthly = df.groupby('month')['amount'].sum()
                fig, ax = plt.subplots(figsize=(10, 4))
                bars = ax.bar(range(len(monthly)), monthly.values, color='#764ba2', alpha=0.7)
                ax.set_xlabel('Month')
                ax.set_ylabel('Total Spent ($)')
                ax.set_xticks(range(len(monthly)))
                ax.set_xticklabels([str(m) for m in monthly.index], rotation=45)
                ax.grid(True, alpha=0.3, axis='y')
                
                # Add value labels on bars
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'${height:.2f}', ha='center', va='bottom', fontsize=9)
                st.pyplot(fig)

