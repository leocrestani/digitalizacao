import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout= "wide")
st.title("Dados")

@st.cache_data
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8')

def formataNumero(valor):
    if valor >= 1_000_000_000:
        return f'{valor / 1_000_000_000:.1f} b'
    if valor >= 1_000_000:
        return f'{valor / 1_000_000:.1f} m'
    if valor >= 1000:
        return f'{valor / 1000:.1f} k'
    
    return str(valor)


data = pd.read_csv('smart_manufacturing_data.csv')

nomes_colunas = {
    'machine': 'Máquina',
    'timestamp': 'Timestamp',
    'temperature': 'Temperatura',
    'vibration': 'Vibração',
    'humidity': 'Umidade',	
    'pressure': 'Pressão',
    'energy_consumption': 'Consumo de Energia',
    'machine_status': 'Status da Máquina',
    'anomaly_flag': 'Flag de Anomalia',
    'predicted_remaining_life': 'Vida Útil Restante Prevista',
    'failure_type': 'Tipo de Falha',
    'downtime_risk': 'Risco de Tempo de Inatividade',
    'maintenance_required': 'Manutenção Necessária'
}

data.rename(columns=nomes_colunas, inplace=True)

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(data.columns), default=list(data.columns))

data_filtrada = data[colunas]

st.dataframe(data_filtrada)
st.markdown( f':gray[{data_filtrada.shape[0]} linhas x {data_filtrada.shape[1]} colunas]' )


st.download_button(
    label='Download CSV',
    data=converte_csv(data),
    file_name='data.csv',
    mime='text/csv',
    icon=':material/download:'
)