import pandas as pd
import osmnx as ox
import networkx as nx
# === Configurações ===
CIDADE = "Recife, Pernambuco, Brasil"
ARQUIVO = "/home/miguel/workspace/projeto_grafos/trabalho-grafos/projeto_grafos/data/bairros_vizinhos.csv"  # coloque o nome do seu arquivo aqui
SAIDA = "/home/miguel/workspace/projeto_grafos/trabalho-grafos/projeto_grafos/data/bairros_vizinhos_tratados.csv"  # coloque o nome do seu arquivo aqui

# === Lê os pares de bairros ===
df = pd.read_csv(ARQUIVO, sep=",")

# === Baixa o grafo da cidade (ruas dirigíveis) ===
print("Carregando mapa da cidade...")
G = ox.graph_from_place(CIDADE, network_type="drive")

resultados = []

# === Itera sobre cada par de bairros ===
for _, row in df.iterrows():
    bairro_a = row["name"]
    bairro_b = row["neighbor"]
    print(f"Processando: {bairro_a} ↔ {bairro_b}")

    try:
        # Pega o ponto mais próximo de cada bairro
        orig_node = ox.distance.nearest_nodes(G, *ox.geocode(f"{bairro_a}, {CIDADE}")[::-1])
        dest_node = ox.distance.nearest_nodes(G, *ox.geocode(f"{bairro_b}, {CIDADE}")[::-1])

        # Calcula rota mais curta entre eles
        route = nx.shortest_path(G, orig_node, dest_node, weight="length")

        # Extrai nomes e tipos de ruas da rota
        ruas = []
        for u, v in zip(route[:-1], route[1:]):
            data = G.edges[u, v, 0]
            nome = data.get("name")
            tipo = data.get("highway")
            if nome:
                ruas.append((nome, tipo))

        # Pega a primeira (ou principal) rua que conecta
        if ruas:
            nome, tipo = ruas[0]
        else:
            nome, tipo = (None, None)

        resultados.append({
            "Bairro": bairro_a,
            "Vizinho": bairro_b,
            "Logradouro": nome,
            "Tipo": tipo
        })

    except Exception as e:
        print(f"Erro ao processar {bairro_a}-{bairro_b}: {e}")
        resultados.append({
            "Bairro": bairro_a,
            "Vizinho": bairro_b,
            "Logradouro": None,
            "Tipo": None
        })

# === Salva resultado ===
pd.DataFrame(resultados).to_csv(SAIDA, index=False)
print(f"✅ Resultado salvo em {SAIDA}")
