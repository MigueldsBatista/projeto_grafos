import pandas as pd
import unidecode

def normalize_text(text):
    if not isinstance(text, str):
        return text
    text = unidecode.unidecode(text)
    return text.lower().strip()


def process_bairros_data(input_csv_path: str, output_csv_path: str) -> None:
    df = pd.read_csv(input_csv_path)

    df_melted = df.melt(
        var_name='microrregiao_cod',
        value_name='bairro'
    )

    df_melted.dropna(subset=['bairro'], inplace=True)
    df_melted = df_melted[df_melted['bairro'].str.strip() != '']

    df_melted['microrregiao'] = df_melted['microrregiao_cod'].str.split('.').str[0]
    
    df_melted['bairro'] = df_melted['bairro'].apply(normalize_text)

    df_final = df_melted[['bairro', 'microrregiao']].drop_duplicates(subset=['bairro']).sort_values(by='bairro')
    df_final.to_csv(output_csv_path, index=False)