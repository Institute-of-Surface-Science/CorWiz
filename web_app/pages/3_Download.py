import os
import streamlit as st
import py7zr
from io import BytesIO
from header import add_header
from footer import add_footer
from helper import display_logo

# Function to truncate long file names
def truncate_filename(file_name: str, max_length: int = 16) -> str:
    """Truncates file name to a maximum length, adding '...' if it's too long."""
    if len(file_name) > max_length:
        return file_name[:max_length - 3] + '...'
    return file_name


# Function to compress all files in a directory into a 7-Zip archive (with README.md)
def download_all_files_as_zip(directory_path: str) -> BytesIO:
    """Compresses all files in a directory into a 7-Zip archive and returns a BytesIO object."""
    zip_buffer = BytesIO()  # Buffer for the zip file in memory
    readme_path = os.path.join("..", 'README.md')

    # Create a 7-Zip archive in the buffer
    with py7zr.SevenZipFile(zip_buffer, 'w') as archive:
        # Add all files in the directory to the archive
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                archive.write(file_path, os.path.relpath(file_path, directory_path))

        # Include README.md in the archive if it exists
        if os.path.exists(readme_path):
            archive.write(readme_path, 'README.md')

    zip_buffer.seek(0)  # Set the buffer's position to the start
    return zip_buffer


# Function to compress a single file (with README.md) into a 7-Zip archive
def compress_single_file_as_zip(file_path: str, readme_path: str) -> BytesIO:
    """Compresses a single file (and README.md) into a 7-Zip archive."""
    zip_buffer = BytesIO()

    # Create a 7-Zip archive in the buffer
    with py7zr.SevenZipFile(zip_buffer, 'w') as archive:
        archive.write(file_path, os.path.basename(file_path))

        # Include README.md in the archive if it exists
        if os.path.exists(readme_path):
            archive.write(readme_path, 'README.md')

    zip_buffer.seek(0)
    return zip_buffer


# Function to list all files in a directory for individual download
def list_files_in_directory(directory_path: str):
    """Returns a list of all files in the given directory."""
    file_list = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list


# Set up the Streamlit page
add_header()

st.markdown("# Download Files")

st.markdown("## License")
ccbysa_url = "https://creativecommons.org/licenses/by-sa/4.0/"

col1, col2 = st.columns([1, 10])
with col1:
    display_logo(
        url="https://creativecommons.org/licenses/by-sa/4.0/",
        img_src="./app/static/logos/CCBYSA.png",
        width="100px",
        alt_text="Creative Commons Attribution Share Alike 4.0 International License",
    )
with col2:
    st.markdown(f"[These files are licensed under a Creative Commons Attribution Share Alike 4.0 International License]({ccbysa_url})")

# Define the directory containing the files to be downloaded
directory_path = "../data/"
readme_path = os.path.join("..", 'README.md')

st.markdown("## Download All Files")
zip_buffer = download_all_files_as_zip(directory_path)
st.download_button(
    label="Download all files as 7-Zip",
    data=zip_buffer,
    file_name="all_files.7z",
    mime="application/x-7z-compressed"
)

st.markdown("## Download Individual Files")
file_list = list_files_in_directory(directory_path)

col1, col2, col3 = st.columns(3)

for i, file_path in enumerate(file_list):
    with open(file_path, 'rb') as file:
        file_name = os.path.basename(file_path)
        truncated_file_name = truncate_filename(file_name)
        zip_buffer = compress_single_file_as_zip(file_path, readme_path)

        # Display in columns
        if i % 3 == 0:
            with col1:
                st.download_button(
                    label=f"Download {truncated_file_name} as 7-Zip",
                    data=zip_buffer,
                    file_name=f"{file_name}.7z",
                    mime="application/x-7z-compressed"
                )
        elif i % 3 == 1:
            with col2:
                st.download_button(
                    label=f"Download {truncated_file_name} as 7-Zip",
                    data=zip_buffer,
                    file_name=f"{file_name}.7z",
                    mime="application/x-7z-compressed"
                )
        else:
            with col3:
                st.download_button(
                    label=f"Download {truncated_file_name} as 7-Zip",
                    data=zip_buffer,
                    file_name=f"{file_name}.7z",
                    mime="application/x-7z-compressed"
                )

# Footer
add_footer()
