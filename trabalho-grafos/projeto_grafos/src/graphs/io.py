import pandas as pd
import unidecode

def normalize_text(text):
    """
    Normaliza uma string: remove acentos, converte para minúsculas e remove espaços extras.
    """
    if not isinstance(text, str):
        return text
    # Usando unidecode para uma normalização mais agressiva, removendo acentos
    text = unidecode.unidecode(text)
    return text.lower().strip()


def process_bairros_data(input_csv_path: str, output_csv_path: str) -> None:
    """
    Lê o arquivo CSV de bairros do Recife, "derrete" (unpivot) os dados,
    normaliza os nomes e salva a lista de bairros únicos com suas microrregiões.

    Args:
        input_csv_path: Caminho para o arquivo bairros_recife.csv.
        output_csv_path: Caminho onde o arquivo processado será salvo.
    """
    # Carrega o CSV original
    df = pd.read_csv(input_csv_path)

    # "Derrete" o DataFrame, transformando as colunas de microrregiões em linhas
    df_melted = df.melt(
        var_name='microrregiao_cod',
        value_name='bairro'
    )

    # Remove linhas onde o nome do bairro é nulo ou vazio
    df_melted.dropna(subset=['bairro'], inplace=True)
    df_melted = df_melted[df_melted['bairro'].str.strip() != '']

    # Extrai o número principal da microrregião (ex: '1.1' -> '1')
    df_melted['microrregiao'] = df_melted['microrregiao_cod'].str.split('.').str[0]
    
    # Normaliza o nome do bairro para padronização
    # Exemplo: "Boa Vista" -> "boa vista"
    df_melted['bairro'] = df_melted['bairro'].apply(normalize_text)

    # Seleciona as colunas finais e remove duplicatas
    # Um bairro pode aparecer em mais de uma coluna original, mas deve ser único.
    df_final = df_melted[['bairro', 'microrregiao']].drop_duplicates(subset=['bairro']).sort_values(by='bairro')
    
    # Salva o resultado em um novo arquivo CSV
    df_final.to_csv(output_csv_path, index=False)