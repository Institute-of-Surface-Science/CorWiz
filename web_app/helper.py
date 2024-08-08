import streamlit as st


def display_logo(url, img_src, alt_text, width="auto", height="auto"):
    simple_id = "img-" + img_src.replace("/", "").replace(".", "")

    image_css = f"""
    width: {width};  # Dynamic width, defaults to 'auto'
    height: {height};  
    max-height:150px;
    object-fit: contain; 
    """

    st.html(
        f"""
        <div id="{simple_id}" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <a href="{url}" target="_blank">
                <img src="{img_src}" alt="{alt_text}" style="{image_css}">
            </a>
        </div>
        """
    )


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<\style>", unsafe_allow_html=True)