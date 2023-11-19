import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
import tempfile
import shutil
import os

# Define the Streamlit app
def main():
    st.title("Baobab Mentorship Applications Stats App")

    # Upload an Excel file
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, header=1)

            # Filter rows based on the condition
            yes_df = df[df['Have you completed the Baobab Mentorship course?'] == 'Yes']

            # Display the filtered DataFrame
            st.subheader("Complete Applications")
            st.write(yes_df)

            # Save the DataFrame into an Excel file
            yes_file_path = 'mastercard_programs.xlsx'
            yes_df.to_excel(yes_file_path, index=False)

            st.success("Data processed and saved successfully!")

            # Create a download link for the Excel file
            st.markdown(get_download_link(yes_file_path, 'mastercard_programs.xlsx'), unsafe_allow_html=True)

            # Display statistics and create plots for 'Mastercard Foundation Programs'
            st.subheader("Statistics and Plots")
            generate_and_display_mastercard_statistics(yes_df)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def get_download_link(file_path, file_name):
    """Generate a download link for a file."""
    href = f'<a href="data:file/{file_path};base64,{base64.b64encode(open(file_path, "rb").read()).decode()}" download="{file_name}">Download {file_name}</a>'
    return href

def generate_and_display_mastercard_statistics(yes_df):
    # Extract and count 'Mastercard Foundation Programs' statistics
    mastercard_counts = yes_df['Which of the following Mastercard Foundation programs, if any, did you participate in (select all that apply) - Selected Choice'].value_counts()
    st.write("Mastercard Foundation Programs Statistics")
    st.write(mastercard_counts)

    # Create and display a bar chart for 'Mastercard Foundation Programs'
    create_and_display_bar_chart(mastercard_counts, "Mastercard Foundation Programs")

    # Save statistics and plot in a PDF document
    pdf_filename = save_mastercard_statistics_and_plot_pdf(mastercard_counts)

    # Provide a download link for the PDF document
    st.markdown(get_download_link(pdf_filename, "Download Mastercard Foundation Programs Statistics PDF"), unsafe_allow_html=True)

def create_and_display_bar_chart(data, title):
    plt.figure(figsize=(8, 4))
    plt.bar(data.index, data.values, color='skyblue')
    plt.xlabel(title)
    plt.xticks(rotation=90)
    plt.ylabel('Count')
    plt.title(f'{title} Distribution')
    st.pyplot(plt)

def save_mastercard_statistics_and_plot_pdf(mastercard_counts):
    pdf_filename = "mastercard_programs_statistics.pdf"

    # Create a temporary directory to store the plot image
    temp_dir = tempfile.mkdtemp()

    try:
        # Create a bar plot for 'Mastercard Foundation Programs' and save as an image
        create_and_save_bar_chart_image(mastercard_counts, "Mastercard Foundation Programs", temp_dir)

        # Create a PDF document
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Define a list to hold document elements
        elements = []

        # Add 'Mastercard Foundation Programs' statistics table to the PDF document
        mastercard_table = create_table_from_series(mastercard_counts, "Mastercard Foundation Programs Statistics")
        elements.append(mastercard_table)

        # Add bar chart image to the PDF document
        chart_image_path = os.path.join(temp_dir, "Mastercard Foundation Programs_chart.png")
        if os.path.exists(chart_image_path):
            img = Image(chart_image_path)
            elements.append(img)

        # Build the PDF document
        doc.build(elements)

        return pdf_filename

    finally:
        # Clean up the temporary directory and remove the plot image
        shutil.rmtree(temp_dir)

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
    plt.xticks(rotation=90)
    plt.ylabel('Count')
    plt.title(f'{title} Distribution')
    plt.savefig(os.path.join(output_dir, f"{title}_chart.png"))
    plt.close()

if __name__ == '__main__':
    main()

