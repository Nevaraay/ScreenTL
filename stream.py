import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.title("Translation History")

# Connect to the database
conn = sqlite3.connect('my_database.db')  # Replace with your DB file
cursor = conn.cursor()

# Read data with original column names
query = "SELECT * FROM translation ORDER BY col1 DESC"
df = pd.read_sql_query(query, conn)

# Save original column names
original_columns = df.columns.tolist()

# Create a copy for display with custom headers
display_columns = ['Datetime', 'Source Language', 'Target Language', 'Source Text', 'Target Text']
df_display = df.copy()
df_display.columns = display_columns

# Show editable table
edited_df = st.data_editor(df_display, num_rows="dynamic", 
                           use_container_width=True)

# Save button
if st.button("Save changes to database"):
    try:
        # Revert columns back to original before saving
        edited_df.columns = original_columns

        # Clear table and insert updated data
        cursor.execute("DELETE FROM translation")
        conn.commit()

        edited_df.to_sql('translation', conn, if_exists='append', index=False)

        st.success("Changes saved to the database successfully.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


st.title("Google API Usage this Month")
st.header("Quota Remaining")

today = datetime.now()
# day = today.day
month = today.month
year = today.year

query = "SELECT sum(col1), sum(col3) FROM usage WHERE month = ? AND year = ?"
data_df = pd.read_sql_query(query, conn, params=(month,year))
data_df['sum(col1)'] = max(int(1000 - data_df['sum(col1)']),0)
data_df['sum(col3)'] = max(int(500000 - data_df['sum(col3)']),0)

st.data_editor(
    data_df,
    column_config={
        "sum(col1)": st.column_config.ProgressColumn(
            "Google Vision Unit",
            help= 'free 1000 units/month',
            format='localized',
            min_value=0,
            max_value=1000,
        ),
        "sum(col3)": st.column_config.ProgressColumn(
            "Google Translate Char",
            help='free 500K chars/month',
            format='compact',
            min_value=0,
            max_value=500000,
        )
    },
    hide_index=True,
)

st.header("Request Graph")
query = "SELECT day, col1, col2 FROM usage WHERE month = ? AND year = ? ORDER BY day DESC"
chart_data = pd.read_sql_query(query, conn, params=(month,year))
chart_data.columns = ["Day", "Vision Request", "Translate Request"]

st.scatter_chart(
    chart_data,
    x="Day",
    y=["Translate Request","Vision Request"],
    color=["#FB00FFC1", "#0000FFD2"],  # Optional
)

st.header("Translate Graph Count")
query = "SELECT day, col3 FROM usage WHERE month = ? AND year = ? ORDER BY day DESC"
chart_data = pd.read_sql_query(query, conn, params=(month,year))
chart_data.columns = ["Day", "Chars"]

st.line_chart(
    chart_data,
    x="Day",
    y="Chars",
    color="#00FF59C1",  # Optional
)

conn.close()


