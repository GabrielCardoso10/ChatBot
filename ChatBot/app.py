import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import flet as ft

# Carrega variáveis de ambiente
load_dotenv()

# Obtém a chave da API Groq
groq_api_key = os.getenv("GROQ_API_KEY")

# Verifica se a chave da API foi encontrada
if not groq_api_key:
    raise ValueError("Chave da API não encontrada. Verifique o arquivo .env.")

# Template do prompt para o modelo de linguagem
template = """
Você é um assistente virtual.
Responda apenas em português.

Entrada: {input}
"""
base_prompt = PromptTemplate(input_variaveis=["input"], template=template)

# Configura o modelo de linguagem
llm = ChatGroq(model_name="llama3-8b-8192", api_key=groq_api_key)

# Memória para manter o histórico de conversas
memoria = ConversationBufferMemory(memory_key="historico_conversa", input_key="input")

# Cadeia do modelo com o prompt e a memória configurados
llm_chain = LLMChain(llm=llm, prompt=base_prompt, memory=memoria)

# Função principal do aplicativo Flet
def main(page: ft.Page):
    # Configuração inicial da página
    page.title = "Cardoso Bot"
    page.bgcolor = ft.colors.BLACK

    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Título do aplicativo
    titulo = ft.Text(
        "CarDosO BoT",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.WHITE,
        text_align=ft.TextAlign.CENTER,
    )

    # Campo de entrada para o usuário
    campo_entrada_usuario = ft.TextField(
        label="Digite sua mensagem",
        hint_text="Escreva aqui...",
        autofocus=True,
        color=ft.colors.BLACK,
        bgcolor=ft.colors.WHITE,
        width=400,
    )

    # Botão de envio
    botao_enviar = ft.ElevatedButton(
        "Enviar",
        on_click=None,
        bgcolor=ft.colors.GREEN_500,
        color=ft.colors.WHITE,
        width=300,
    )

    # Texto de resposta do assistente
    texto_resposta = ft.Text(
        "Assistente: Olá, como posso ajudar?",
        size=18,
        color=ft.colors.WHITE,
        text_align=ft.TextAlign.CENTER,
    )

    # Função que é chamada ao clicar no botão "Enviar"
    def ao_clicar_enviar(e):
        # Obtém o texto digitado pelo usuário
        entrada_usuario = campo_entrada_usuario.value

        # Verifica se o usuário deseja encerrar o assistente
        if entrada_usuario.lower() in ["sair", "exit", "quit"]:
            texto_resposta.value = "Assistente: Encerrando o assistente. Até logo!"
            page.update()
            return

        # Obtém a resposta do modelo de linguagem
        resposta = llm_chain.invoke(input=entrada_usuario)
        if isinstance(resposta, dict) and 'text' in resposta:
            texto_resposta.value = f"Assistente: {resposta['text']}"
        else:
            texto_resposta.value = "Assistente: Não foi possível gerar uma resposta."

        # Atualiza a página com a nova resposta
        page.update()

        return

    # Associa a função ao botão "Enviar"
    botao_enviar.on_click = ao_clicar_enviar

    # Adiciona os elementos à página
    page.add(titulo, campo_entrada_usuario, botao_enviar, texto_resposta)

    # Atualiza a página
    page.update()

# Executa o aplicativo
ft.app(target=main)
