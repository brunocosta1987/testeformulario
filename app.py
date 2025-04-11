import streamlit as st
import sqlite3

# Função para conectar ao banco de dados
def conectar_db():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

# Função para inserir dados
def inserir_usuario(nome, sobrenome, email):
    conn = conectar_db()
    c = conn.cursor()
    c.execute("INSERT INTO usuarios (nome, sobrenome, email) VALUES (?, ?, ?)", (nome, sobrenome, email))
    conn.commit()
    conn.close()

# Função para consultar dados
def consultar_usuarios():
    conn = conectar_db()
    c = conn.cursor()
    c.execute("SELECT nome, sobrenome, email FROM usuarios")
    dados = c.fetchall()
    conn.close()
    return dados

# Estilo e animações
st.markdown("""
    <style>
        .sidebar .stSelectbox > div {
            transition: transform 0.2s ease;
        }
        .sidebar .stSelectbox > div:hover {
            transform: scale(1.03);
        }
        .sidebar .stSelectbox > div:active {
            transform: scale(0.97);
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("<h1 style='text-align: center;'>Cadastro de Usuários</h1>", unsafe_allow_html=True)

# Menu lateral
menu = st.sidebar.selectbox("Menu", ["Cadastrar", "Consultar"])

# Tela de cadastro
if menu == "Cadastrar":
    st.subheader("Cadastrar Novo Usuário")
    nome = st.text_input("Nome")
    sobrenome = st.text_input("Sobrenome")
    email = st.text_input("Email")

    if st.button("Salvar"):
        if nome and sobrenome and email:
            inserir_usuario(nome, sobrenome, email)
            st.success("Usuário cadastrado com sucesso!")
        else:
            st.warning("Por favor, preencha todos os campos.")

# Tela de consulta
elif menu == "Consultar":
    st.subheader("Lista de Usuários Cadastrados")
    usuarios = consultar_usuarios()

    if usuarios:
        df = pd.DataFrame(usuarios, columns=["Nome", "Sobrenome", "Email"])
        st.dataframe(df)

        # Botão para download como Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Usuarios')
        output.seek(0)

        st.download_button(
            label="📥 Baixar como Excel",
            data=output,
            file_name="usuarios.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Nenhum usuário cadastrado ainda.")


