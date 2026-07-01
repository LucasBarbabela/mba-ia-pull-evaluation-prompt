import json
from pathlib import Path

from utils import get_llm

# Ajuste este import conforme seu projeto
from langchain_core.load import load
import yaml

def main():
    prompt_path = "prompts/bug_to_user_story_v2.yaml"

    if not Path(prompt_path).exists():
        print(f"❌ Prompt não encontrado: {prompt_path}")
        return

    dataset_path = "datasets/bug_to_user_story.jsonl"

    if not Path(dataset_path).exists():
        print(f"❌ Dataset não encontrado: {dataset_path}")
        return

    print("=" * 80)
    print("TESTE LOCAL DO PROMPT")
    print("=" * 80)

    with open(prompt_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    prompt = load(data)
    llm = get_llm()

    chain = prompt | llm

    with open(dataset_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            example = json.loads(line)

            inputs = example["inputs"]
            reference = example["outputs"]["reference"]

            print(f"\n{'=' * 80}")
            print(f"EXEMPLO {i}")
            print(f"{'=' * 80}")

            print("\n🐞 BUG REPORT:")
            print(inputs["bug_report"])

            try:
                response = chain.invoke(inputs)

                answer = (
                    response.content
                    if hasattr(response, "content")
                    else str(response)
                )

                print("\n🤖 RESPOSTA GERADA:")
                print(answer)

                print("\n📋 REFERÊNCIA:")
                print(reference)

            except Exception as e:
                print(f"\n❌ Erro ao executar prompt: {e}")

            # Limite para não executar o dataset inteiro
            if i >= 3:
                break

    print("\n✅ Teste concluído")


if __name__ == "__main__":
    main()