import os
import matplotlib.pyplot as plt
import pandas as pd


def gerar_grafico_faturamento(df_relatorio, caminho_imagem):
    """Gera e salva um gráfico de barras com o faturamento por produto."""
    plt.figure(figsize=(8, 5))

    # Criar gráfico de barras
    barras = plt.bar(
        df_relatorio["produto"],
        df_relatorio["faturamento_total"],
        color="#2b5c8f",
    )

    # Adicionar títulos e rótulos
    plt.title("Faturamento Total por Produto", fontsize=14, fontweight="bold")
    plt.xlabel("Produto", fontsize=11)
    plt.ylabel("Faturamento (R$)", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Adicionar os valores numéricos em cima de cada barra
    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2.0,
            altura,
            f"R$ {altura:,.2f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()

    # Salvar a imagem no disco
    plt.savefig(caminho_imagem, dpi=300)
    plt.close()
    print(f"Gráfico gerado com sucesso em: '{caminho_imagem}'")


def processar_relatorio_vendas(caminho_entrada, caminho_saida_csv, caminho_imagem_png):
    # 1. EXTRAÇÃO
    if not os.path.exists(caminho_entrada):
        print(f"[Erro] O arquivo '{caminho_entrada}' não foi encontrado.")
        return

    print("Lendo dados de entrada...")
    df = pd.read_csv(caminho_entrada)

    # 2. TRANSFORMAÇÃO
    print("Transformando os dados...")
    df["faturamento_total"] = df["quantidade"] * df["preco_unitario"]

    relatorio = (
        df.groupby("produto")
        .agg(
            total_unidades_vendidas=("quantidade", "sum"),
            faturamento_total=("faturamento_total", "sum"),
            preco_medio_venda=("preco_unitario", "mean"),
        )
        .reset_index()
    )

    relatorio = relatorio.sort_values(by="faturamento_total", ascending=False)

    # 3. CARREGAMENTO (CSV e Imagem PNG)
    relatorio.to_csv(caminho_saida_csv, index=False)
    print(f"Relatório CSV gerado em: '{caminho_saida_csv}'")

    # Gerar o gráfico visual
    gerar_grafico_faturamento(relatorio, caminho_imagem_png)

    print("\n--- Resumo das Vendas ---")
    print(relatorio.to_string(index=False))


if __name__ == "__main__":
    ARQUIVO_ENTRADA = "vendas_brutas.csv"
    ARQUIVO_SAIDA = "relatorio_final.csv"
    IMAGEM_GRAFICO = "faturamento_produtos.png"

    processar_relatorio_vendas(ARQUIVO_ENTRADA, ARQUIVO_SAIDA, IMAGEM_GRAFICO)