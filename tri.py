import streamlit as st
import os
rootFolder = os.getcwd()
rootUser = os.getcwd().split('\\')

rootFolder = os.getcwd()
rootUser = rootFolder.split('\\')

ABEIUser = '\\'.join(rootUser[0:3]) + "\\ABEIOneDrive"
try:
    os.path.exists(ABEIUser)   
except Exception as e:
    ABEIUser = '\\'.join(rootUser[0:3])
# C:\Users\usuario\ABEI Energy\Prom. Estudios Técnicos - Documentos\01- ESPAÑA
if not os.path.exists(ABEIUser):
    ABEIUser = '\\'.join(rootUser[0:3])


rootJson = ABEIUser + "\\ABEI Energy\\P.E.TECNICOS - ITALY\\08.- GRID ITALIA\\E-dist json\\3. Sources\\E-dist"

def main():
    st.title(rootJson)
    number = st.number_input("Choose a number between 1 and 10", min_value=1, max_value=10, step=1)
    
    if st.button("Allocate Slots"):
        allocate_slots(number)

def allocate_slots(number):
    st.subheader(f"Allocating {number} slots for input values")
    
    for i in range(1, number + 1):
        value = st.text_input(f"Slot {i}")
        st.write(f"Value entered in Slot {i}: {value}")

if __name__ == '__main__':
    main()
