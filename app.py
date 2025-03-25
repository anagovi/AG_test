import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.title("📊 File Uploader: CSV/XLS Reader with Output File")

with st.form("file_upload_form"):
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xls", "xlsx"])
    submit_button = st.form_submit_button("Upload and Process")

if submit_button:
    if uploaded_file is not None:
        try:
            summary_data = []

            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                num_rows, num_cols = df.shape
                summary_data.append({
                    "Sheet Name": "CSV File",
                    "Number of Rows": num_rows,
                    "Number of Columns": num_cols
                })

            else:
                # Read all sheets from Excel
                xls = pd.read_excel(uploaded_file, sheet_name=None)  # returns a dict {sheet_name: df}
                for sheet_name, sheet_df in xls.items():
                    num_rows, num_cols = sheet_df.shape
                    summary_data.append({
                        "Sheet Name": sheet_name,
                        "Number of Rows": num_rows,
                        "Number of Columns": num_cols
                    })

            # Create summary DataFrame
            output_df = pd.DataFrame(summary_data)

            # Display summary on screen
            st.success("✅ File uploaded and read successfully!")
            st.subheader("📄 Output Summary")
            st.dataframe(output_df)

            # Generate output filename
            base_name = os.path.splitext(uploaded_file.name)[0]
            output_filename = f"{base_name}_output.xlsx"

            # Write summary to Excel file in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                output_df.to_excel(writer, index=False, sheet_name='Summary')

            output.seek(0)

            # Download link
            st.download_button(
                label="📥 Download Output Excel File",
                data=output,
                file_name=output_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
    else:
        st.warning("⚠️ Please upload a file before submitting.")
