import os
import requests
from bs4 import BeautifulSoup

# Configurações do Telegram (Vem das variáveis secretas do GitHub)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")


def checar_estoque():
    # URL do painel do InfoSaúde
    url = "https://info.saude.df.gov.br/saude-do-cidadao/painel-infosaude-farmacias-de-alto-custo/estoque-de-medicamentos/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        resposta = requests.get(url, headers=headers, timeout=30)
        # Nota: Caso o Power BI bloqueie a requisição direta via requests,
        # o status precisará ser extraído da API interna do Power BI.
        # Para este escopo, validamos a estrutura de transição de estado.

        # --- Lógica de varredura fictícia baseada no HTML retornado ---
        # Substitua pela busca exata do componente se necessário
        soup = BeautifulSoup(resposta.text, "html.parser")

        # Exemplo de lógica de checagem (ajustável conforme a API/HTML do GDF)
        # Vamos assumir por segurança que o padrão é "Sem Estoque" se não acharmos explicitamente o positivo
        status_atual = "Sem Estoque"

        # (Insira aqui o parse específico do iframe do Power BI se necessário)
        # Se encontrar a linha "Asa Sul" + "Somatropina" + "Disponível", status_atual = "Com Estoque"

        return status_atual

    except Exception as e:
        print(f"Erro ao acessar o site: {e}")
        return "Erro"


def main():
    status_atual = checar_estoque()

    if status_atual == "Erro":
        return

    # Lendo o status anterior para evitar repetições inúteis
    arquivo_status = "status_anterior.txt"
    status_anterior = "Sem Estoque"

    if os.path.exists(arquivo_status):
        with open(arquivo_status, "r") as f:
            status_anterior = f.read().strip()

    print(f"Status Anterior: {status_anterior} | Status Atual: {status_atual}")

    # Condição principal: Mudou de 'Sem Estoque' para 'Com Estoque'
    if status_anterior == "Sem Estoque" and status_atual == "Com Estoque":
        mensagem = (
            "🔔 *ALERTA DE ESTOQUE!* 🔔\n\n"
            "O medicamento *SOMATROPINA 12 UI* mudou de status e consta como *DISPONÍVEL* na unidade *Asa Sul*.\n\n"
            "Verifique no site: https://info.saude.df.gov.br"
        )
        enviar_telegram(mensagem)

    # Atualiza o arquivo de histórico para a próxima rodada
    with open(arquivo_status, "w") as f:
        f.write(status_atual)


if __name__ == "__main__":
    main()
