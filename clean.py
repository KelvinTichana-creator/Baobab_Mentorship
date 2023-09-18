import streamlit as st
import pandas as pd
import base64

# Define the Streamlit app
def main():
    st.title("Baobab Mentorship Applications Cleaning App")

    # Upload an Excel file
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)

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

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def get_download_link(file_path, file_name):
    """Generate a download link for a file."""
    href = f'<a href="data:file/{file_path};base64,{base64.b64encode(open(file_path, "rb").read()).decode()}" download="{file_name}">Download {file_name}</a>'
    return href

if __name__ == '__main__':
    main()

