import pandas as pd
import osmnx as ox
import networkx as nx

# === Configurações ===
CIDADE = "Recife, Pernambuco, Brasil"
ARQUIVO = "/home/miguel/workspace/projeto_grafos/trabalho-grafos/projeto_grafos/data/bairros_vizinhos.csv"
SAIDA = "/home/miguel/workspace/projeto_grafos/trabalho-grafos/projeto_grafos/data/bairros_vizinhos_tratados.csv"

# === Mapeamento de pesos ===
mapeamento_pesos = {
    "motorway": 0.8,
    "motorway_link": 0.8,
    "trunk": 1.0,
    "trunk_link": 1.0,
    "primary": 1.2,
    "primary_link": 1.2,
    "secondary": 1.5,
    "secondary_link": 1.5,
    "tertiary": 1.8,
    "tertiary_link": 1.8,
    "residential": 2.0,
    "service": 2.5,
    "living_street": 2.5,
    "pedestrian": 3.0,
    "track": 3.0,
    "unclassified": 2.2
}

# Normalizar tipo (ex.: primary_link → primary)
def normalizar_tipo(tipo):
    if isinstance(tipo, list):
        # pega o mais "forte": motorway > trunk > primary > secondary > tertiary > residential > service...
        prioridade = ["motorway", "trunk", "primary", "secondary", "tertiary", "residential", "service"]
        for p in prioridade:
            if p in tipo:
                return p
        return tipo[0]
    if "_link" in tipo:
        return tipo.replace("_link", "")
    return tipo

# === Lê os pares de bairros ===
df = pd.read_csv(ARQUIVO, sep=",")

print("Carregando mapa da cidade...")
G = ox.graph_from_place(CIDADE, network_type="drive")

resultados = []

# === Itera ===
for _, row in df.iterrows():
    bairro_a = row["name"]
    bairro_b = row["neighbor"]
    print(f"Processando: {bairro_a} ↔ {bairro_b}")

    try:
        orig_node = ox.distance.nearest_nodes(G, *ox.geocode(f"{bairro_a}, {CIDADE}")[::-1])
        dest_node = ox.distance.nearest_nodes(G, *ox.geocode(f"{bairro_b}, {CIDADE}")[::-1])

        route = nx.shortest_path(G, orig_node, dest_node, weight="length")

        ruas = []
        for u, v in zip(route[:-1], route[1:]):
            data = G.edges[u, v, 0]
            nome = data.get("name")
            tipo = data.get("highway")

            if nome:
                ruas.append((nome, tipo))

        # === Remove nomes repetidos ===
        ruas_unicas = []
        vistos = set()
        for nome, tipo in ruas:
            if nome not in vistos:
                ruas_unicas.append((nome, tipo))
                vistos.add(nome)

        if ruas_unicas:
            nome_escolhido, tipo_bruto = ruas_unicas[0]
            tipo_norm = normalizar_tipo(tipo_bruto)

            peso = mapeamento_pesos.get(tipo_norm, None)
        else:
            nome_escolhido, tipo_norm, peso = None, None, None

        resultados.append({
            "Bairro": bairro_a,
            "Vizinho": bairro_b,
            "Logradouro": nome_escolhido,
            "Tipo_normalizado": tipo_norm,
            "Peso": peso
        })

    except Exception as e:
        print(f"Erro ao processar {bairro_a}-{bairro_b}: {e}")
        resultados.append({
            "Bairro": bairro_a,
            "Vizinho": bairro_b,
            "Logradouro": None,
            "Tipo_normalizado": None,
            "Peso": None
        })

# === Salva ===
pd.DataFrame(resultados).to_csv(SAIDA, index=False)
print(f"✅ Resultado salvo em {SAIDA}")
