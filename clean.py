import streamlit as st
import pandas as pd
import base64
import re
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
import matplotlib.pyplot as plt
import tempfile
import shutil
import os
# Define the Streamlit app
def main():
    st.title("Baobab Mentorship Applications Cleaning App")

    # Upload an Excel file
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, header=1)

            # Load the last processed row index from a file or database
            try:
                with open('last_processed_row.txt', 'r') as file:
                    last_processed_row_index = int(file.read())
            except FileNotFoundError:
                last_processed_row_index = 0

            # Filter rows starting from the last processed row index
            new_rows_df = df[df.index > last_processed_row_index]

            # Split the filtered DataFrame into two based on the condition
            yes_df = new_rows_df[new_rows_df['Have you completed the Baobab Mentorship course?'] == 'Yes']
            no_df = new_rows_df[new_rows_df['Have you completed the Baobab Mentorship course?'] == 'No']

            # Display the filtered DataFrames
            st.subheader("Complete Applications")
            st.write(yes_df)

            st.subheader("Incomplete Applications")
            st.write(no_df)

            # Save the separate DataFrames into different Excel files
            yes_file_path = 'clean_applications.xlsx'
            no_file_path = 'incomplete_applications.xlsx'

            yes_df.to_excel(yes_file_path, index=False)
            no_df.to_excel(no_file_path, index=False)

            # Update the last processed row index to the maximum index of the current data
            last_processed_row_index = df.index.max()

            # Save the last processed row index back to the file
            with open('last_processed_row.txt', 'w') as file:
                file.write(str(last_processed_row_index))

            st.success("Data processed and saved successfully!")

            # Create download links for the Excel files
            st.markdown(get_download_link(yes_file_path, 'clean_applications.xlsx'), unsafe_allow_html=True)
            st.markdown(get_download_link(no_file_path, 'incomplete_applications.xlsx'), unsafe_allow_html=True)

            # Display statistics and create plots
            st.subheader("Statistics and Plots")
            generate_and_display_statistics(df, new_rows_df)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def extract_age_ranges(series):
    age_ranges = []
    pattern = r'(\d+-\d+)'
    for value in series:
        matches = re.findall(pattern, str(value))
        age_ranges.extend(matches)
    return pd.Series(age_ranges)

def get_download_link(file_path, file_name):
    """Generate a download link for a file."""
    href = f'<a href="data:file/{file_path};base64,{base64.b64encode(open(file_path, "rb").read()).decode()}" download="{file_name}">Download {file_name}</a>'
    return href

def generate_and_display_statistics(df, yes_df):
    # Extract and count 'Gender' statistics from after processed row
    gender_counts = yes_df['Gender   (We match from a gender binary of male/female. Please answer this question to ensure that we match you appropriately with a mentor.)'].value_counts()
    st.write("Gender Statistics (After Processed Row):")
    st.write(gender_counts)


    # Extract and count 'User Language' statistics from after processed row
    # language_counts = yes_df['User Language'].value_counts()
    language_counts = yes_df[yes_df['Have you completed the Baobab Mentorship course?'] == 'Yes']['User Language'].value_counts()
    st.write("Language Statistics (After Processed Row):")
    st.write(language_counts)

    # Extract and count 'Country of birth' statistics from after processed row
    country_counts = yes_df['Country of birth'].value_counts()
    st.write("Country Statistics (After Processed Row):")
    st.write(country_counts)

    # Extract all age ranges and count occurrences from after processed row
    age_ranges = extract_age_ranges(yes_df['Age'])
    age_range_counts = age_ranges.value_counts().reset_index()
    age_range_counts.columns = ['Age Range', 'Count']
    st.write("Age Range Statistics (After Processed Row):")
    st.write(age_range_counts)

    # Create and display bar charts for 'Gender', 'User Language', and 'Country of birth'
    create_and_display_bar_chart(gender_counts, "Gender")
    create_and_display_bar_chart(language_counts, "User Language")
    create_and_display_bar_chart(country_counts, "Country of Birth")

    # Save statistics and plots in a PDF document
    pdf_filename = save_statistics_and_plots_pdf(gender_counts, language_counts, country_counts, age_range_counts)

    # Provide a download link for the PDF document
    st.markdown(get_download_link(pdf_filename, "Download Statistics and Plots PDF"), unsafe_allow_html=True)

def create_and_display_bar_chart(data, title):
    plt.figure(figsize=(8, 4))
    plt.bar(data.index, data.values, color='skyblue')
    plt.xlabel(title)
    plt.ylabel('Count')
    plt.title(f'{title} Distribution')
    st.pyplot(plt)

def save_statistics_and_plots_pdf(gender_counts, language_counts, country_counts, age_range_counts):
    pdf_filename = "statistics_and_plots.pdf"

    # Create a temporary directory to store plot images
    temp_dir = tempfile.mkdtemp()

    try:
        # Create bar plots for 'Gender', 'User Language', and 'Country of birth' and save as images
        create_and_save_bar_chart_image(gender_counts, "Gender", temp_dir)
        create_and_save_bar_chart_image(language_counts, "User Language", temp_dir)
        create_and_save_bar_chart_image(country_counts, "Country of Birth", temp_dir)

        # Create a PDF document
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Define a list to hold document elements
        elements = []

        # Add 'Gender' statistics table to the PDF document
        gender_table = create_table_from_series(gender_counts, "Gender Statistics")
        elements.append(gender_table)

        # Add 'User Language' statistics table to the PDF document
        language_table = create_table_from_series(language_counts, "Language Statistics")
        elements.append(language_table)

        # Add 'Country of birth' statistics table to the PDF document
        country_table = create_table_from_series(country_counts, "Country Statistics")
        elements.append(country_table)

        # Add 'Age Range' statistics table to the PDF document
        age_range_table = create_table_from_dataframe(age_range_counts, "Age Range Statistics")
        elements.append(age_range_table)

        # Add bar chart images to the PDF document
        for chart_title in ["Gender", "User Language", "Country of Birth"]:
            chart_image_path = os.path.join(temp_dir, f"{chart_title}_chart.png")
            if os.path.exists(chart_image_path):
                img = Image(chart_image_path)
                elements.append(img)

        # Build the PDF document
        doc.build(elements)

        return pdf_filename

    finally:
        # Clean up the temporary directory and remove plot images
        shutil.rmtree(temp_dir)
def create_table_from_dataframe(dataframe, title):
    data = [dataframe.columns.values.astype(str).tolist()] + dataframe.values.tolist()
    t = Table(data)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    return t
def create_table_from_series(data, title):
    table_data = [(key, value) for key, value in data.items()]
    table_data.insert(0, ("Category", "Count"))
    t = Table(table_data)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    return t
def create_and_save_bar_chart_image(data, title, output_dir):
    plt.figure(figsize=(8, 4))
    plt.bar(data.index, data.values, color='skyblue')
    plt.xlabel(title)
    plt.ylabel('Count')
    plt.title(f'{title} Distribution')
    plt.savefig(os.path.join(output_dir, f"{title}_chart.png"))
    plt.close()

if __name__ == '__main__':
    main()

