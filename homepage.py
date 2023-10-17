import streamlit as st

class HomePage:
    def render(self):
        st.markdown("""
        ## Welcome to Home Page

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel sapien sed risus vestibulum lacinia. Donec posuere ac ante a efficitur.

        ---
        """)
        col1, col2 = st.columns(2)
        with col1:
            st.image("logo1.png", width=250)
        with col2:
            st.markdown("""
            Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Pellentesque non dictum lorem.
            """)
            st.image("logo2.png", width=250)
            st.image("logo3.png", width=250)
            st.image("logo4.png", width=250)
