import streamlit as st


footer_string = """
<style>
footer{
    visibility: visible;
}
footer:after{
    content: 'Powered by: OpenAI, Langchain, and Streamlit';
    display:block;
    position:relative;
    color:black;
    padding:5px;
    top:3px; 
}
</style>
"""


def footer():
    st.markdown(footer_string, unsafe_allow_html=True)
