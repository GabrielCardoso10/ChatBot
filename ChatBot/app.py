import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import flet as ft

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Chave da API não encontrada. Verifique o arquivo .env.")

template = """
Você é um assistente virtual.
Responda apenas em português.

Entrada: {input}
"""
base_prompt = PromptTemplate(input_variaveis=["input"], template=template)

llm = ChatGroq(model_name="llama3-8b-8192", api_key=groq_api_key)

memoria = ConversationBufferMemory(memory_key="historico_conversa", input_key="input")

llm_chain = LLMChain(llm=llm, prompt=base_prompt, memory=memoria)

def main(page: ft.Page):
    page.title = "Cardoso Bot"
    page.bgcolor = ft.colors.BLACK

    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    titulo = ft.Text(
        "CarDosO BoT",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.WHITE,
        text_align=ft.TextAlign.CENTER,
    )

    campo_entrada_usuario = ft.TextField(
        label="Digite sua mensagem",
        hint_text="Escreva aqui...",
        autofocus=True,
        color=ft.colors.BLACK,
        bgcolor=ft.colors.WHITE,
        width=400,
    )

    botao_enviar = ft.ElevatedButton(
        "Enviar",
        on_click=None,
        bgcolor=ft.colors.GREEN_500,
        color=ft.colors.WHITE,
        width=300,
    )

    texto_resposta = ft.Text(
        "Assistente: Olá, como posso ajudar?",
        size=18,
        color=ft.colors.WHITE,
        text_align=ft.TextAlign.CENTER,
    )

    def ao_clicar_enviar(e):
        entrada_usuario = campo_entrada_usuario.value

        if entrada_usuario.lower() in ["sair", "exit", "quit"]:
            texto_resposta.value = "Assistente: Encerrando o assistente. Até logo!"
            page.update()
            return

        resposta = llm_chain.invoke(input=entrada_usuario)
        if isinstance(resposta, dict) and 'text' in resposta:
            texto_resposta.value = f"Assistente: {resposta['text']}"
        else:
            texto_resposta.value = "Assistente: Não foi possível gerar uma resposta."

        page.update()

        return

    botao_enviar.on_click = ao_clicar_enviar

    page.add(titulo, campo_entrada_usuario, botao_enviar, texto_resposta)

    page.update()

ft.app(target=main)
