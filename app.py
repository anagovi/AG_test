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
            # Read uploaded file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("✅ File uploaded and read successfully!")
            num_rows, num_cols = df.shape
            st.write(f"**Number of rows:** {num_rows}")
            st.write(f"**Number of columns:** {num_cols}")

            # Prepare output data
            output_df = pd.DataFrame({
                "Metric": ["Number of Rows", "Number of Columns"],
                "Value": [num_rows, num_cols]
            })

            # Display the output dataframe on screen
            st.subheader("📄 Output Summary")
            st.dataframe(output_df)

            # Generate output filename
            base_name = os.path.splitext(uploaded_file.name)[0]
            output_filename = f"{base_name}_output.xlsx"

            # Write to in-memory Excel file
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

