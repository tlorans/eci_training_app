import streamlit as st

def session_page(title, description, pdf_path=None):
    """
    Reusable template for each training session page.
    """

    st.title(title)

    st.write(description)

    if pdf_path is not None:
        st.write("### Download Summary")
        try:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download PDF summary",
                    data=f,
                    file_name=pdf_path.split("/")[-1],
                    mime="application/pdf",
                )
        except FileNotFoundError:
            st.error(f"PDF not found at path: {pdf_path}")
