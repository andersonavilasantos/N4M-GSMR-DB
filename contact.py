import streamlit as st

class ContactPage:
    def __init__(self):
        pass  # No data passed for the contact page
    
    def render(self):
        st.markdown("""
        ## Contact Us

        The MAG-based Genome-Scale Metabolic Reconstruction Database was developed by:
        - **Ulisses Nunes da Rocha**
        - **Avila Santos Anderson Paulo**
        - **Robson Parmezan Bonidia**
        - **Sanchita Kamath**
        - **Joao Pedro Saraiva**
        - **Stefanía Magnúsdóttir**

        The development took place at the **Helmholz-Zentrum for Environmental Research** (Leipzig, Germany) and the **University of São Paulo** (São Carlos, Brazil).

        ### What is the reason of your contact?

        - **Feedback?**  
          Feel free to use our Feedback Form to help us improve our database. You can also send an email to Dr. Ulisses Nunes da Rocha at [ulisses.rocha@ufz.de](mailto:ulisses.rocha@ufz.de).

        - **Questions?**  
          If our "Home" guide does not cover your questions, please post your question in the User Group for others to benefit.

        - **Other regards?**  
          For other regards or questions please contact Dr. Ulisses Nunes da Rocha at [ulisses.rocha@ufz.de](mailto:ulisses.rocha@ufz.de).
        """)

