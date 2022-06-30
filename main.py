import streamlit as st

def main():
    with st.sidebar.header("Source Data Selection"):
        st.sidebar.write("select dataset")




if __name__ == "__main__":
    st.set_page_config(page_title="UCT Prague accelerated experiments application", layout = "wide")
    main()