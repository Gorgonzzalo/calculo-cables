import streamlit as st
from aereas import *
from coordinates import *


"""
# Sizing cables calculation
"""
optionCable = st.radio("# Choose an option", ("Aerial line", "Underground cable"))

if optionCable == "Aerial line":

    """
    ##### Parametres of the project
    """
    potPOI = st.text_input("Enter the desired power @ POI (MW)")

    col1, col2 = st.columns(2)

    elevation = ''
    pressure = ''


    with col1:
        latitude = st.text_input("Enter the latitude")

    with col2:
        longitude = st.text_input("Enter the longitude")

    if (latitude != "") & (longitude != ""):
        elevation, pressure = get_elevationAndPressure(latitude, longitude)
        elevation = round(elevation, 2)
        pressure = round(pressure, 2)
        st.write("The elevation of the project is ", elevation, "m")
        st.write("The elevation of the project is ", pressure, "cmHg")

    longLinea = st.text_input("Enter the longitude of the line (km)")
    voltage = st.text_input("Enter the voltage of the line (kV)")
    maxVoltage = st.text_input("Enter the maximum voltage of the line (kV)")

    col3, col4 = st.columns(2)

    with col3:
        voltageDrop = st.slider("Maximum % voltage drop", 0.0, 10.0, 0.0, step  =0.1)

    with col4:
        powerLoss = st.slider("Maximum % power loss", 0.0, 10.0, 0.0, step  =0.1)

    if (elevation!="") & (potPOI!="") & (voltage!="") & (longLinea!="") & (pressure!="") & (maxVoltage!="") & (voltageDrop!=0.0) & (powerLoss!=0.0):
        dicAereas = dict(elevacion = elevation, potPOI = potPOI,tensionAereaLinea = voltage,longAereaLinea = longLinea, presion = pressure, tensionMaxAereaLinea = maxVoltage , caidaTension =  voltageDrop,perdidaPotencia = powerLoss )

        dicAereas = lineasAereas(dicAereas)

        try:
            st.write("Your cable is: ",dicAereas['faseNAereaCable'], "cable",dicAereas['faseAereaCable'], "size",dicAereas['sizemm2'], "mm2" )
        except Exception as e:
            pass



elif optionCable == "Option 2":
    slider_value = st.slider("Choose a value", 0, 100, step=1)
    st.write("You chose:", slider_value)
else:
    st.write("Please select a cable")

