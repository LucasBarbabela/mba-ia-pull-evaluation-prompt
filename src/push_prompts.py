"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    try:
        client = Client()
        response = client.push_prompt("bug_to_user_story_v2", object=prompt_data)
        print(f"Prompt pushado com sucesso para o LangSmith Hub: {response}")
        return response
    except Exception as e:
        print(f"Erro ao pushar prompt para o LangSmith Hub: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list[str]]:
    errors = []

    prompt_dict = prompt_data.get("__dict__")

    if not prompt_dict:
        errors.append("Campo '__dict__' não encontrado")
        return False, errors

    if not prompt_dict.get("input_variables"):
        errors.append("input_variables não encontrado")

    messages = prompt_dict.get("messages")

    if not isinstance(messages, list) or not messages:
        errors.append("messages inválido ou vazio")

    return len(errors) == 0, errors


def main(): 
    check_env_vars(["LANGSMITH_API_KEY"])
    yaml = load_yaml("prompts/bug_to_user_story_v2.yml")
    validate_prompt(yaml)
    push_prompt_to_langsmith("bug_to_user_story_v2", yaml)


if __name__ == "__main__":
    sys.exit(main())
