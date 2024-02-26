import streamlit as st
import pyscript

# Store a variable in local storage
st.write(pyscript.write("localStorage.setItem('my_data', 'Hello from Python!')"))

# Retrieve a variable from local storage
retrieved_data = pyscript.eval("localStorage.getItem('my_data')")
st.write("Retrieved data:", retrieved_data)
