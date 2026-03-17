import streamlit as st
from utils.data_processor import (
    load_csv,
    get_summary,
    get_statistics,
    get_column_options,
    get_groupby_summary,
)
from utils.chart_generator import (
    bar_chart,
    line_chart,
    pie_chart,
    horizontal_bar_chart,
)
from utils.pdf_generator import generate_pdf

st.set_page_config(
    page_title="DataForge",
    page_icon="🔥",
    layout="wide",
)
# Main title
st.title("🔥 DataForge")
st.markdown("Upload any CSV file and generate a professional PDF report instantly.")

# Sidebar
st.sidebar.header("Controls")
st.sidebar.markdown("---")

# File uploader
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV file",
    type=["csv"],
)
if uploaded_file is None:
    st.info("👈 Upload a CSV file from the sidebar to get started!")
    st.stop()

df = load_csv(uploaded_file)
summary = get_summary(df)
numeric_cols, text_cols = get_column_options(df)
st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rows", summary["total_rows"])

with col2:
    st.metric("Total Columns", summary["total_columns"])

with col3:
    st.metric("Missing Values", summary["missing_values"])

st.markdown("---")
st.subheader("Data Preview")
st.dataframe(df.head(10), use_container_width=True)

st.subheader("Descriptive Statistics")
stats_df = get_statistics(df)
if not stats_df.empty:
    st.dataframe(stats_df, use_container_width=True)
else:
    st.warning("No numeric columns found in your data.")

st.markdown("---")
st.sidebar.markdown("### Chart Settings")

chart_type = st.sidebar.selectbox(
    "Chart Type",
    ["Bar Chart", "Line Chart", "Pie Chart", "Horizontal Bar Chart"]
)

if text_cols:
    group_col = st.sidebar.selectbox(
        "Group By (text column)",
        text_cols
    )
else:
    st.sidebar.warning("No text columns found!")
    group_col = None

if numeric_cols:
    value_col = st.sidebar.selectbox(
        "Value (numeric column)",
        numeric_cols
    )
else:
    st.sidebar.warning("No numeric columns found!")
    value_col = None
st.subheader("Chart Preview")

if group_col and value_col:
    grouped_df = get_groupby_summary(df, group_col, value_col)

    if chart_type == "Bar Chart":
        chart = bar_chart(grouped_df, group_col, f"Total_{value_col}")
    elif chart_type == "Line Chart":
        chart = line_chart(grouped_df, group_col, f"Total_{value_col}")
    elif chart_type == "Pie Chart":
        chart = pie_chart(grouped_df, group_col, f"Total_{value_col}")
    elif chart_type == "Horizontal Bar Chart":
        chart = horizontal_bar_chart(grouped_df, group_col, f"Total_{value_col}")

    st.image(chart, use_container_width=True)
else:
    st.warning("Please select valid columns to generate a chart.")

st.markdown("---")
st.subheader("Generate Report")

report_title = st.text_input(
    "Report Title",
    value="My Data Report"
)

if st.button("🔥 Generate PDF Report", use_container_width=True):
    if group_col and value_col:
        with st.spinner("Generating your report..."):
            grouped_df = get_groupby_summary(df, group_col, value_col)

            chart1 = bar_chart(grouped_df, group_col, f"Total_{value_col}")
            chart2 = pie_chart(grouped_df, group_col, f"Total_{value_col}")

            charts = [
                (f"{value_col} by {group_col}", chart1),
                (f"{value_col} distribution", chart2),
            ]

            pdf = generate_pdf(df, stats_df, charts, report_title)

        st.success("✅ Report generated successfully!")

        st.download_button(
            label="📥 Download PDF Report",
            data=pdf,
            file_name=f"{report_title.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.error("Please select valid columns first!")