import streamlit as st
import pandas as pd


from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib
from joblib import load
from utils import RenomearColunasTransf, MultiLabelEncoder, YesNoToBinaryTransformer, MinMax, OrdinalEncodingTransformer, DummyEncoderTransformer, ColumnsToIntTransformer


#importando base (alterar para caminho do GIT)
base = pd.read_csv(r"D:\PosFIAP\ArquivosTC4\Obesity.csv", sep=',')
#exmplo:
#dados = pd.read_csv('https://raw.githubusercontent.com/alura-tech/alura-tech-pos-data-science-credit-scoring-streamlit/main/df_clean.csv')


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

#family_history
input_historico = st.radio('Histórico familiar de excesso de peso?',["***Sim***","***Não***"])

#FAVC
input_alimento_calorico = st.radio('Consumo frequente de alimentos muito calóricos?',["***Sim***","***Não***"])

#FCVC
input_vegetais = st.selectbox('Frequência de consumo de vegetais nas refeições?', ("Selecione...", "Raramente", "Às vezes", "Sempre"))

#NCP
st.write('### Número de refeições principais por dia:')
input_refeicoes = float(st.slider('Selecione a quantidade:', 1, 4))

#CAEC
input_lanches = st.selectbox('Consumo de lanches entre as refeições?', ("Selecione...", "Não consome", "Às vezes", "Frequentemente", "Sempre"))

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
input_alcoolica = st.selectbox('Consumo de bebida alcoólica?', ("Selecione...", "Não bebe", "Às vezes", "Frequentemente", "Sempre"))

#MTRANS
input_transporte = st.selectbox('Meio de transporte habitual', ("Selecione...", "Carro", "Moto", "Bicicleta", "Transporte Público", "A pé"))


# ===========================================================
# 🔘 Botão e tratamento dos dados
# ===========================================================



# Separando os dados em treino e teste
def data_split(df):
    treino_df, teste_df = train_test_split(df, test_size=0.2, random_state=42)
    return treino_df.reset_index(drop=True), teste_df.reset_index(drop=True)

treino_df, teste_df = data_split(base)

def pipeline_teste(df):

    pipeline = Pipeline([
        ('renomear', RenomearColunasTransf()),
        ('min_max_scaler',MinMax()),
        ('ordinal_feature', OrdinalEncodingTransformer()),
        ('label_encoding', MultiLabelEncoder(
            columns=[
                'historico_familiar',
                'calorias_frequente',
                'fuma',
                'genero',
                'monitora_calorias'
            ]
        )),
        ('transformarBinario',YesNoToBinaryTransformer()),
        ('onehot_transporte', DummyEncoderTransformer()),
        ('ajustandoColunasTransporte',ColumnsToIntTransformer()),
    # ... outros transformers ou modelos ...
    ])
    df_pipeline = pipeline.fit_transform(df)
    return df_pipeline


if st.button("Adicionar Pesquisa"):

    campos_invalidos = []

    # Verificar se todos foram preenchidos corretamente
    if input_vegetais == "Selecione...":
        campos_invalidos.append("Frequência de vegetais")
    if input_lanches == "Selecione...":
        campos_invalidos.append("Lanches")
    if input_alcoolica == "Selecione...":
        campos_invalidos.append("Bebida alcoólica")
    if input_transporte == "Selecione...":
        campos_invalidos.append("Transporte")

    # Se houver campos não preenchidos
    if campos_invalidos:
        st.error(f"⚠️ Por favor, preencha todos os campos obrigatórios: {', '.join(campos_invalidos)}")
    else:
        # Dicionários de conversão da tela de streamlit para poder adicionar o valor no dataframe
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
            transporte_num,
            0 #####TRATAR OBESIDADE#####
        ]

        #Criando novo paciente
        paciente_predict_df = pd.DataFrame([nova_pesquisa],columns=teste_df.columns)

        #Concatenando novo paciente ao dataframe dos dados de teste
        teste_novo_paciente  = pd.concat([teste_df,paciente_predict_df],ignore_index=True)

        #Aplicando a pipeline
        teste_novo_paciente = pipeline_teste(teste_novo_paciente)

        #retirando a coluna target
        cliente_pred = teste_novo_paciente.drop(['nvl_obsidade_ord'], axis=1)

        model = joblib.load('RandomForest.joblib')
        final_pred = model.predict(cliente_pred)

        # Mostra resultado
        #st.success("✅ Dados adicionados com sucesso!")
        st.write("**Lista tratada:**", nova_pesquisa)


        st.write("**PREDIIICAOOOOO:**", final_pred[-1])
