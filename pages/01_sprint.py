import streamlit as st
import pandas as pd
import plotly.express as px

# Função para converter horas em dias e horas
def formatar_tempo(horas):
    dias = int(horas // 24)
    horas_restantes = int(horas % 24)
    return f"{dias} dias, {horas_restantes} horas"

# CSS para centralizar o conteúdo
st.markdown(
    """
    <style>
    .center-content {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .divider {
        height: 1px;
        width: 100%;
        background-color: #e0e0e0;
        margin: 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    file_name = uploaded_file.name

    # Resumo da análise
    st.markdown(f'<div class="file-name"><h2>Resumo da Análise: {file_name}</h2></div>', unsafe_allow_html=True)

    total_tarefas = len(df)
    tarefas_concluidas = len(df[df['Estado'].str.lower() == 'concluído'])
    pontos_concluidos = df[df['Estado'].str.lower() == 'concluído']['Campo personalizado (Story Points)'].sum()
    pontos_totais = df['Campo personalizado (Story Points)'].sum()

    st.markdown(
        f"""
        <div class="center-content">
            <h4>Total de Tarefas: {total_tarefas}</h4>
            <h4>Tarefas concluídas: {tarefas_concluidas}</h4>
            <h4>Pontos totais: {pontos_totais}</h4>
            <h4>Pontos de entregues: {pontos_concluidos}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    done = df[df['Estado'].str.lower() == 'concluído'.lower()]

    # Quantidade de tarefas por peso
    if 'Campo personalizado (Story Points)' in df.columns:
        tarefas_por_peso = df['Campo personalizado (Story Points)'].value_counts().reset_index()
        tarefas_por_peso.columns = ['Peso (Story Points)', 'Quantidade']
        tarefas_por_peso = tarefas_por_peso.sort_values(by='Peso (Story Points)')

        fig_tarefas_por_peso = px.bar(tarefas_por_peso, 
                                      x='Peso (Story Points)', 
                                      y='Quantidade', 
                                      title='Quantidade de tarefas por peso',
                                      labels={'Quantidade': 'Quantidade de Tarefas'})

        st.plotly_chart(fig_tarefas_por_peso)

        # Adiciona linha divisória
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    else:
        st.write("A coluna 'Campo personalizado (Story Points)' não está presente no arquivo CSV.")


    ####################################################################################################################################    


    # Quantidade de Tarefas por Etiqueta
    if 'Etiquetas' in df.columns:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="center-content">', unsafe_allow_html=True)
            tarefas_por_etiqueta = df['Etiquetas'].value_counts().reset_index()
            tarefas_por_etiqueta.columns = ['Etiquetas', 'Quantidade']

            # Quantidade de Tarefas por Status como Tabela
            done_tasks = len(df[df['Estado'].str.lower() == 'concluído'.lower()])
            todo_tasks = len(df[df['Estado'].str.lower() == 'a fazer'.lower()])
            progress_tasks = len(df[df['Estado'].str.lower() == 'em progresso'.lower()])
            deploy_tasks = len(df[df['Estado'].str.lower() == 'ready to deploy'.lower()])
            review_tasks = len(df[df['Estado'].str.lower() == 'review'.lower()])
            validate_tasks = len(df[df['Estado'].str.lower() == 'validate'.lower()])
            acceptance_tasks = len(df[df['Estado'].str.lower() == 'acceptance'.lower()])

            total_tasks = todo_tasks + progress_tasks + deploy_tasks + review_tasks + acceptance_tasks + validate_tasks + done_tasks

            st.table(pd.DataFrame({
                'Status': ['A Fazer', 'Em Progresso', 'Code Review', 'Review', 'Aceitação', 'Pronto para Entregar', 'Concluído', 'Total'],
                'Quantidade': [todo_tasks, progress_tasks, validate_tasks, review_tasks, acceptance_tasks, deploy_tasks, done_tasks, total_tasks]
            }))
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="center-content">', unsafe_allow_html=True)
            fig_tarefas_por_etiqueta = px.pie(tarefas_por_etiqueta, 
                                              names='Etiquetas', 
                                              values='Quantidade', 
                                              title='Quantidade de tarefas por etiqueta')

            st.plotly_chart(fig_tarefas_por_etiqueta)
            st.markdown('</div>', unsafe_allow_html=True)

        # Adiciona linha divisória
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    else:
        st.write("A coluna 'Etiquetas' não está presente no arquivo CSV.")


    ####################################################################################################################################


    # Tarefas por Responsável (Todas as Tarefas)
    if 'Responsável' in df.columns:
        tarefas_por_responsavel = df['Responsável'].value_counts().reset_index()
        tarefas_por_responsavel.columns = ['Responsável', 'Quantidade']

        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        fig_responsavel = px.bar(tarefas_por_responsavel, x='Responsável', y='Quantidade', title='Quantidade de tarefas por Responsável')
        st.plotly_chart(fig_responsavel)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    else:
        st.write("A coluna 'Responsável' não está presente no arquivo CSV.")

    ####################################################################################################################################

    # Tarefas Concluídas por Responsável
    if 'Estado' in df.columns and 'Responsável' in df.columns:
        tarefas_concluidas = df[df['Estado'].str.lower() == 'concluído']

        if not tarefas_concluidas.empty:
            concluidas_por_responsavel = tarefas_concluidas['Responsável'].value_counts().reset_index()
            concluidas_por_responsavel.columns = ['Responsável', 'Quantidade']

            st.markdown('<div class="center-content">', unsafe_allow_html=True)
            fig_responsavel_concluidas = px.bar(concluidas_por_responsavel, x='Responsável', y='Quantidade', title='Tarefas Concluídas por Responsável')
            st.plotly_chart(fig_responsavel_concluidas)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        else:
            st.write("Não há tarefas concluídas para exibir a distribuição por responsável.")
    else:
        st.write("As colunas 'Estado' e 'Responsável' não estão presentes no arquivo CSV.")

    ####################################################################################################################################

    # Tipos de problema e suas quantidades
    tipo_problema_counts = df['Tipo de Problema'].value_counts().reset_index()
    tipo_problema_counts.columns = ['Tipo de Problema', 'Quantidade']

    color_discrete_map = {
        'historia': '#6CB844',  # verde claro
        'subarefa': '#4AAFE7',  # azul claro
        'problema': '#DE4B3B',  # vermelho
        'tarefa': '#1C84C4'     # azul escuro
    }

    fig_tipo_problema = px.pie(tipo_problema_counts, 
                               names='Tipo de Problema', 
                               values='Quantidade', 
                               title='Tipos de problema',
                               color='Tipo de Problema',
                               color_discrete_map=color_discrete_map)

    # Gráfico
    st.plotly_chart(fig_tipo_problema)

    # Adiciona linha divisória
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


    ####################################################################################################################################


    # Pontos atribuidos por usuário
    if 'Campo personalizado (Story Points)' in df.columns:
        pontos_por_usuario = df.groupby('Responsável')['Campo personalizado (Story Points)'].sum().reset_index()
        soma_pontos_sprint = df['Campo personalizado (Story Points)'].sum()

        fig_pontos_por_usuario = px.bar(pontos_por_usuario, x='Responsável', y='Campo personalizado (Story Points)',
                                        title='Pontos atribuidos por usuário', labels={'Campo personalizado (Story Points)': 'Story Points'})

        st.plotly_chart(fig_pontos_por_usuario)


    ####################################################################################################################################


    # Pontos entregues por usuário e soma total dos pontos (considerando apenas tarefas concluídas)
    if 'Campo personalizado (Story Points)' in df.columns:
        # Filtra as tarefas concluídas
        tarefas_concluidas = df[df['Estado'].str.lower() == 'concluído']

        # Calcula os pontos por usuário para tarefas concluídas
        pontos_por_usuario = tarefas_concluidas.groupby('Responsável')['Campo personalizado (Story Points)'].sum().reset_index()

        # Soma total dos pontos das tarefas concluídas
        soma_pontos_sprint = tarefas_concluidas['Campo personalizado (Story Points)'].sum()

        # Criação do gráfico
        fig_pontos_por_usuario = px.bar(pontos_por_usuario, x='Responsável', y='Campo personalizado (Story Points)',
                                        title='Pontos entregues por usuário', labels={'Campo personalizado (Story Points)': 'Story Points'})

        st.plotly_chart(fig_pontos_por_usuario)


        # Exibe a soma total dos pontos
        st.write(f"Soma total dos pontos no Sprint (apenas concluídas): {soma_pontos_sprint}")

else:
    st.write("Por favor, carregue um arquivo CSV.")
