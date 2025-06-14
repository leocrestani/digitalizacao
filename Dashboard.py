import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard",
    layout= "wide")

st.title("Dashboard de Visão de Máquinas")

data = pd.read_csv('smart_manufacturing_data.csv')

st.sidebar.title('Filtros')
with st.sidebar.expander("Filtros de Data"):
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data = data.sort_values(by='timestamp')
    data_inicio = data['timestamp'].min()
    data_fim = data['timestamp'].max()
    selected_dates = st.sidebar.date_input("Selecione o intervalo de datas", [data_inicio, data_fim], min_value=data_inicio, max_value=data_fim)
    data = data[(data['timestamp'] >= pd.to_datetime(selected_dates[0])) & (data['timestamp'] <= pd.to_datetime(selected_dates[1]))]

with st.sidebar.expander("Filtros de Status da Máquina"): 
    status_maquinas = data['machine_status'].unique()
    selected_status = st.sidebar.multiselect('Selecione os Status das Máquinas', status_maquinas, default=status_maquinas)
    data = data[data['machine_status'].isin(selected_status)]

with st.sidebar.expander("Configurações Avançadas"):
    show_anomalies = st.checkbox("Exibir Anomalias", value=True)
    show_failures = st.checkbox("Exibir Falhas", value=True)
    data = data[data['anomaly_flag'] == "Yes"] if show_anomalies else data

aba1, aba2, aba3, aba4, aba5 = st.tabs(["Visão Geral", "Status das máquinas", "Correlação entre Features", "Análise de Anomalias", "Análise de Falhas"])

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
    st.header("Correlação entre Features")
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['timestamp'] = data['timestamp'].astype(int) / 10**9
    features = ["timestamp", "temperature", "vibration", "humidity", "pressure", "energy_consumption", "predicted_remaining_life", "downtime_risk"]
    data_feature = data[features]
    data_feature = data_feature.dropna() 
    corr = data_feature.corr(method='pearson')
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r',
                         title="Correlação entre Features")
    fig_corr.update_layout(xaxis_title="Features", yaxis_title="Features")
    st.plotly_chart(fig_corr, use_container_width=True)

with aba4:
    st.header("Análise de Anomalias")
    anomalies = data[data['anomaly_flag'] == "Yes"]
    fig_anomalies = px.scatter(anomalies, x='timestamp', y='temperature', color='machine',
                                title="Anomalias Detectadas por Máquina",
                                labels={"timestamp": "Timestamp", "temperature": "Temperatura", "machine": "Máquina"})
    st.plotly_chart(fig_anomalies, use_container_width=True)

with aba5:
    st.header("Análise de Falhas")
    data_falha = data[data['failure_type'] != "Normal"]
    failure_counts = data_falha['failure_type'].value_counts()
    fig_failures = px.bar(failure_counts, x=failure_counts.index, y=failure_counts.values,
                          title="Tipos de Falhas por Máquina",
                          labels={"failure_type": "Tipo de Falha", "value": "Contagem"},
                          color_discrete_sequence=px.colors.qualitative.Dark2)
    fig_failures.update_layout(xaxis_title="Tipo de Falha", yaxis_title="Contagem")
    st.plotly_chart(fig_failures, use_container_width=True)