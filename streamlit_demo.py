import streamlit as st
import pandas as pd
from main_demo import analyze_data, get_database_schema
import json
import sys
from io import StringIO

st.set_page_config(
    page_title="AI Data Analyst (DEMO)",
    page_icon="chart_with_upwards_trend",
    layout="wide"
)

st.title("AI Data Analyst - DEMO MODE")
st.markdown("**Demo Mode:** Pattern-based SQL generation (no Ollama required)")
st.info("For the real AI version with Deepseek, install Ollama and use streamlit run streamlit_app.py")

# Sidebar with schema info
with st.sidebar:
    st.header("Database Schema")
    schema = get_database_schema()

    for table, columns in schema.items():
        with st.expander(f"Table: {table}"):
            col_info = []
            for col in columns:
                col_info.append(f"- **{col['name']}** ({col['type']})")
            st.markdown("\n".join(col_info))

    st.markdown("---")
    st.markdown("**Demo Queries:**")
    st.markdown("""
    - Show customers from Mumbai
    - Total sales by category
    - Expensive products
    - Cheap products
    - All orders
    - Order details
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Ask a Question")
    user_query = st.text_input(
        "What would you like to know about your data?",
        placeholder="e.g., Show me all customers from Mumbai",
        key="user_query"
    )

with col2:
    st.subheader("Quick Examples")
    examples = [
        "Show customers from Mumbai",
        "Total sales by category",
        "Expensive products",
        "Order details",
        "All products"
    ]
    for example in examples:
        if st.button(example, key=example):
            user_query = example

if user_query:
    with st.spinner("Processing your query..."):
        try:
            # Suppress print statements from main_demo.py
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            sql_query, result = analyze_data(user_query)

            sys.stdout = old_stdout

            # Display SQL Query
            st.subheader("Generated SQL Query")
            st.code(sql_query, language="sql")

            # Display Results
            if result["success"]:
                if result["data"]:
                    st.subheader("Results")
                    df = pd.DataFrame(result["data"])
                    st.dataframe(df, use_container_width=True)

                    # Display statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Rows", len(result["data"]))
                    with col2:
                        st.metric("Total Columns", len(result["columns"]))
                    with col3:
                        st.metric("Status", "Success")

                    # Download option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No results found for your query.")
            else:
                st.error(f"Error: {result['error']}")

        except Exception as e:
            st.error(f"Error processing query: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
**Switch to AI Mode:**
1. Install Ollama from https://ollama.ai
2. Run: `ollama serve`
3. Run: `ollama pull deepseek-r1:8b`
4. Use: `streamlit run streamlit_app.py`
""")
