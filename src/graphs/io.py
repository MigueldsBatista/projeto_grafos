import pandas as pd
import unidecode
import ast

def normalize_text(text):
    return unidecode.unidecode(text).lower().strip() if isinstance(text, str) else text


df = pd.read_csv('bairros_qgis.csv')
df.head()

# drop useless columns

df = df.drop(columns=['full_id', 'osm_id', 'osm_type', 'admin_level', 'wikidata', 'wikipedia', 'place', 'boundary', 'type', 'landuse'], errors='ignore')
df_pairs = df.assign(neighbor=df['neighbors'].apply(ast.literal_eval)).explode('neighbor')

df_pairs = df_pairs.dropna(
    subset=['neighbor']
    ).reset_index(drop=True)[['name', 'neighbor']]

df_pairs.head()
df.info()
pd.DataFrame(df_pairs).to_csv('bairros_vizinhos.csv', index=False)


