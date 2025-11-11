import streamlit as st
import pandas as pd


st.write('# Pesquisa sobre obesidade')


#Gender
st.write('### Por favor, preencher os dados da Pesquisa:')
input_genero = st.radio('Selecione o Sexo:',["***Masculino***","***Feminino***"])

#Age
input_idade = float(st.slider('Selecione sua idade:', 14, 61))

#Height
input_altura = st.number_input(
    "Insira sua altura (em cm)",
    min_value=50,      # Altura mínima razoável
    max_value=300,     # Altura máxima razoável
    value=170,         # Valor padrão
    step=1,            # Passo de 1 cm
    format="%d"        # Garante que o valor seja um inteiro
)

#Weight
input_peso = st.number_input(
    "Insira seu peso (em kg)",
    min_value=50,      # Altura mínima razoável
    max_value=300,     # Altura máxima razoável
    value=80,         # Valor padrão
    step=1            # Passo de 1 kg
)

###st.write('## IMC:'+ input_altura/input_peso)

#family_history
input_historico = st.radio('Histórico familiar de excesso de peso?',["***Sim***","***Não***"])

#FAVC
input_alimento_calorico = st.radio('Consumo frequente de alimentos muito calóricos?',["***Sim***","***Não***"])

#FCVC
input_vegetais = st.selectbox('Frequência de consumo de vegetais nas refeições?',("Raramente", "Às vezes", "Sempre"))

#NCP
st.write('### Número de refeições principais por dia:')
input_refeicoes = float(st.slider('Selecione a quantidade:', 1, 4))

#CAEC
input_lanches = st.selectbox('Consumo de lanches/comes entre as refeições?',("Não consome", "Às vezes", "Frequentemente", "Sempre"))

#SMOKE
input_fuma = st.radio('Hábito de fumar?',["***Sim***","***Não***"])

#CH2O
input_agua = st.radio('Consumo diário de água?',["***< 1 L/dia***","***1–2 L/dia***","***2 L/dia***"])

#SCC
input_ingestao_calorica = st.radio('Monitora a ingestão calórica diária?',["***Sim***","***Não***"])

#FAF
input_atividade_fisica = st.radio('Frequência semanal de atividade física:',["***Nenhuma***","***~1–2×/sem***"
                                                                             ,"***~3–4×/sem***","***5×/sem ou mais***"])

#TUE
input_dispositivo_eletronico = st.radio('Tempo diário usando dispositivos eletrônicos',["***~0–2 h/dia***","***~3–5 h/dia***","***> 5 h/dia***"])

#CALC
input_alcoolica = st.selectbox('Consumo de bebida alcoólica?',("Não bebe", "Às vezes", "Frequentemente", "Sempre"))

#MTRANS
input_transporte = st.selectbox('Meio de transporte habitual',("Carro", "Moto", "Bicicleta", "Transporte Público", "A pé"))


# ===========================================================
# 🔘 Botão e tratamento dos dados
# ===========================================================

if st.button("Adicionar Pesquisa"):
    # Dicionários de conversão para valores numéricos
    map_binario = {"***Sim***": "yes", "***Não***": "no"}
    map_genero = {"***Masculino***": "Male", "***Feminino***": "Female"}
    map_vegetais = {"Raramente": 1, "Às vezes": 2, "Sempre": 3}
    map_lanches = {"Não consome": "no", "Às vezes": "Sometimes", "Frequentemente": "Frequently", "Sempre": "Always"}
    map_agua = {"***< 1 L/dia***": 1, "***1–2 L/dia***": 2, "***2 L/dia***": 3}
    map_atividade = {"***Nenhuma***": 0, "***~1–2×/sem***": 1, "***~3–4×/sem***": 2, "***5×/sem ou mais***": 3}
    map_dispositivo = {"***~0–2 h/dia***": 0, "***~3–5 h/dia***": 1, "***> 5 h/dia***": 2}
    map_alcoolica = {"Não bebe": "no", "Às vezes": "Sometimes", "Frequentemente": "Frequently", "Sempre": "Always"}
    map_transporte = {"Carro": "Automobile", "Moto": "Motorbike", "Bicicleta": "Bike", "Transporte Público": "Public_Transportation", "A pé": "Walking"}

    # Conversão dos campos
    sexo_num = map_genero[input_genero]
    historico_num = map_binario[input_historico]
    calorico_num = map_binario[input_alimento_calorico]
    vegetais_num = map_vegetais[input_vegetais]
    lanches_num = map_lanches[input_lanches]
    fuma_num = map_binario[input_fuma]
    agua_num = map_agua[input_agua]
    calorias_num = map_binario[input_ingestao_calorica]
    atividade_num = map_atividade[input_atividade_fisica]
    dispositivo_num = map_dispositivo[input_dispositivo_eletronico]
    alcoolica_num = map_alcoolica[input_alcoolica]
    transporte_num = map_transporte[input_transporte]

    # Monta lista final tratada
    nova_pesquisa = [
        0,  # pode ser ID
        sexo_num,
        input_idade,
        input_altura,
        input_peso,
        historico_num,
        calorico_num,
        vegetais_num,
        input_refeicoes,
        lanches_num,
        fuma_num,
        agua_num,
        calorias_num,
        atividade_num,
        dispositivo_num,
        alcoolica_num,
        transporte_num
    ]

    # Mostra resultado
    st.success("✅ Dados adicionados com sucesso!")
    st.write("**Lista tratada:**", nova_pesquisa)