"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    username = os.getenv("USERNAME_LANGSMITH_HUB", "")
    prompt = hub.pull(f"{username}/bug_to_user_story_v1")

    system_prompt = prompt.messages[0].prompt.template
    user_prompt = prompt.messages[1].prompt.template

    data = {
        "bug_to_user_story_v1": {
            "description": "Prompt inicial de baixa qualidade para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }

    save_path = Path("prompts/bug_to_user_story_v1.yml")
    save_yaml(data, save_path)
    print(f"   ✓ Prompt salvo em {save_path}")


def main():
    """Função principal"""
    required_vars = ["LANGSMITH_API_KEY", "LANGSMITH_ENDPOINT", "LANGSMITH_PROJECT", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1
    print_section_header("Pulling Prompts from LangSmith Prompt Hub")
    pull_prompts_from_langsmith()
    print("Prompt pulled e salvo em prompts/bug_to_user_story_v1.yml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
