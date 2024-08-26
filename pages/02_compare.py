import streamlit as st
import pandas as pd
import plotly.express as px

# Criação de colunas para upload de arquivos
col1, col2 = st.columns(2)

with col1:
    st.subheader("Arquivo 1")
    uploaded_file1 = st.file_uploader("Escolha o primeiro arquivo CSV", type="csv", key="file1")

with col2:
    st.subheader("Arquivo 2")
    uploaded_file2 = st.file_uploader("Escolha o segundo arquivo CSV", type="csv", key="file2")

if uploaded_file1 is not None and uploaded_file2 is not None:
    # Obter o nome dos arquivos
    file_name1 = uploaded_file1.name
    file_name2 = uploaded_file2.name
    
    df1 = pd.read_csv(uploaded_file1)
    df2 = pd.read_csv(uploaded_file2)

    # Função para contar tarefas por status
    def contar_tarefas_por_status(df, status):
        return len(df[df['Estado'].str.lower() == status.lower()])

    status_list = ['concluído', 'a fazer', 'em progresso', 'ready to deploy']
    comparacao_status = {'Status': [], file_name1: [], file_name2: []}

    for status in status_list:
        comparacao_status['Status'].append(status.capitalize())
        comparacao_status[file_name1].append(contar_tarefas_por_status(df1, status))
        comparacao_status[file_name2].append(contar_tarefas_por_status(df2, status))

    df_comparacao_status = pd.DataFrame(comparacao_status)

    # Gráfico de comparação de status
    fig_comparacao_status = px.bar(df_comparacao_status, x='Status', y=[file_name1, file_name2], 
                                   barmode='group', title='Tarefas por Status')
    st.plotly_chart(fig_comparacao_status)

    # Comparação de tipos de problema
    tipo_problema1 = df1['Tipo de Problema'].value_counts().reset_index()
    tipo_problema1.columns = ['Tipo de Problema', file_name1]
    
    tipo_problema2 = df2['Tipo de Problema'].value_counts().reset_index()
    tipo_problema2.columns = ['Tipo de Problema', file_name2]
    
    df_comparacao_problema = pd.merge(tipo_problema1, tipo_problema2, on='Tipo de Problema', how='outer').fillna(0)

    # Gráfico de comparação de tipos de problema
    fig_comparacao_problema = px.bar(df_comparacao_problema, x='Tipo de Problema', y=[file_name1, file_name2], 
                                     barmode='group', title='Tipos de Problema')
    st.plotly_chart(fig_comparacao_problema)

    # Cálculo do total de pontos das tarefas entregues
    def total_pontos_tarefas_entregues(df):
        tarefas_entregues = df[df['Estado'].str.lower() == 'concluído']
        return tarefas_entregues['Campo personalizado (Story Points)'].sum() if not tarefas_entregues.empty else 0

    total_pontos1 = total_pontos_tarefas_entregues(df1)
    total_pontos2 = total_pontos_tarefas_entregues(df2)

    df_total_pontos = pd.DataFrame({
        'Arquivo': [file_name1, file_name2],
        'Total de Pontos Entregues': [total_pontos1, total_pontos2]
    })

    # Gráfico do total de pontos das tarefas entregues
    fig_total_pontos = px.bar(df_total_pontos, x='Arquivo', y='Total de Pontos Entregues', 
                             title='Total de Pontos das Tarefas Entregues')
    st.plotly_chart(fig_total_pontos)

else:
    st.write("Por favor, carregue os dois arquivos CSV.")
