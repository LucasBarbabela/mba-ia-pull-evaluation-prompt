"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

from pathlib import Path

import yaml
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.load import dumpd
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():   
    client = Client()

    prompt = client.pull_prompt(
        "leonanluppi/bug_to_user_story_v1",
        dangerously_pull_public_prompt=True
    )

    # Save the prompt locally
    save_path = Path("prompts/bug_to_user_story_v1.yml")
    prompt_dict = dumpd(prompt)
    save_yaml(prompt_dict, save_path)

    print(f"Prompt salvo em: {save_path}")


def main():
    pull_prompts_from_langsmith()


if __name__ == "__main__":
    main()
