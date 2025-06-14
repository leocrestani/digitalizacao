import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard",
    layout= "wide")

st.title("Dashboard de Visão de Máquinas")

data = pd.read_csv('smart_manufacturing_data.csv')

aba1, aba2, aba3 = st.tabs(["Visão Geral", "Status das máquinas", "Aba3"])

with aba1:
    st.header("Visão Geral")
    data_media = data.groupby("machine")[["temperature", "vibration", "humidity", "pressure"]].mean()

    # temperature
    fig_temp = px.bar(data_media, x=data_media.index, y="temperature", title="Média de Temperatura por Máquina", labels={"temperature": "Temperatura", "machine": "Máquina"})
    fig_temp.update_layout(xaxis_title="Máquina", yaxis_title="Temperatura", xaxis_tickangle=-45)
    st.plotly_chart(fig_temp, use_container_width=True)

    # vibration
    fig_vib = px.bar(data_media, x=data_media.index, y="vibration", title="Média de Vibração por Máquina", labels={"vibration": "Vibração", "machine": "Máquina"}, color_discrete_sequence=["#ff7f0e"])
    fig_vib.update_layout(xaxis_title="Máquina", yaxis_title="Vibração", xaxis_tickangle=-45)
    st.plotly_chart(fig_vib, use_container_width=True)

    # humidity
    fig_hum = px.bar(data_media, x=data_media.index, y="humidity", title="Média de Umidade por Máquina", labels={"humidity": "Umidade", "machine": "Máquina"}, color_discrete_sequence=["#2ca02c"])
    fig_hum.update_layout(xaxis_title="Máquina", yaxis_title="Umidade", xaxis_tickangle=-45)
    st.plotly_chart(fig_hum, use_container_width=True)

    # pressure
    fig_pres = px.bar(data_media, x=data_media.index, y="pressure", title="Média de Pressão por Máquina", labels={"pressure": "Pressão", "machine": "Máquina"}, color_discrete_sequence=["#d62728"])
    fig_pres.update_layout(xaxis_title="Máquina", yaxis_title="Pressão", xaxis_tickangle=-45)
    st.plotly_chart(fig_pres, use_container_width=True)

with aba2:
    st.header("Status das máquinas")
    status_counts = data['machine_status'].value_counts(normalize=True) * 100
    fig_status = px.pie(status_counts, values=status_counts.values, names=status_counts.index, 
                        title="Percentual dos Status das Máquinas",
                        labels={"machine_status": "Status", "value": "Percentual"},
                        color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_status.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_status, use_container_width=True)

with aba3:
    st.header("Aba3")