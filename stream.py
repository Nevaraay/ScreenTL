import streamlit as st
import pandas as pd
import translation_history as th
from datetime import datetime


st.set_page_config(
    page_title="Translation History",
    page_icon="🧊",
    layout="wide"
)
st.title("Translation History")

# Initialize button state
if "button_state" not in st.session_state:
    st.session_state.button_state = False

def toggle():
    st.session_state.button_state = not st.session_state.button_state

# Connect to the database
history = th.TranslationHistory()
history.insert_bar()

# Read data with original column names
query = "SELECT * FROM translation ORDER BY col1 DESC"
df = pd.read_sql_query(query, history.conn)

# Save original column names
original_columns = df.columns.tolist()

# Create a copy for display with custom headers
display_columns = ['Datetime', 'Source Language', 'Target Language', 'Source Text', 'Target Text']
df_display = df.copy()
df_display.columns = display_columns

st.button("Edit table", on_click=toggle)
if st.session_state.button_state is True: # make edit table button toggle-able
    # Show editable table
    edited_df = st.data_editor(df_display, num_rows="dynamic", 
                            use_container_width=True,
                            disabled=False
                            )
else:
    edited_df = st.data_editor(df_display, num_rows="fixed", 
                            use_container_width=True,
                            disabled=True,
                            hide_index=True)

# Save button
if st.button("Save table changes to database"):
    try:
        # Revert columns back to original before saving
        edited_df.columns = original_columns

        # Clear table and insert updated data
        history.cursor.execute("DELETE FROM translation")
        history.conn.commit()

        edited_df.to_sql('translation', history.conn, if_exists='append', index=False)

        st.success("Changes saved to the database successfully.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


st.title("Google APIs Usage this Month")
st.header("Quota Remaining")

# Check date for today
today = datetime.now()
month = today.month
year = today.year


# Display remaining Google APIs remaining quota
query = "SELECT sum(col1), sum(col3) FROM usage WHERE month = ? AND year = ?"
data_df = pd.read_sql_query(query, history.conn, params=(month,year))
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
    disabled=True
)

st.header("Request Graph")
query = "SELECT day, col1, col2 FROM usage WHERE month = ? AND year = ? ORDER BY day DESC"
chart_data = pd.read_sql_query(query, history.conn, params=(month,year))
chart_data.columns = ["Day", "Vision Request", "Translate Request"]

st.scatter_chart(
    chart_data,
    x="Day",
    y=["Translate Request","Vision Request"],
    color=["#FB00FFC1", "#0000FFD2"],  # Optional
)

st.header("Translate Graph Count")
query = "SELECT day, col3 FROM usage WHERE month = ? AND year = ? ORDER BY day DESC"
chart_data = pd.read_sql_query(query, history.conn, params=(month,year))
chart_data.columns = ["Day", "Chars"]

st.line_chart(
    chart_data,
    x="Day",
    y="Chars",
    color="#00FF59C1",  # Optional
)

history.conn.close()


