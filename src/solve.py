# Contém a lógica de execução principal (ler dados, rodar algoritmo, salvar resultados)

# Exemplo:
# from graphs.io import carregar_grafo
# from graphs.algorithms import bfs, dijkstra
# from graphs.graph import Grafo



import json
import pandas as pd
from graphs.graph import Graph

def calculate_density(order: int, size: int) -> float:
    
    if order < 2:
        return 0.0
    return (2 * size) / (order * (order - 1))

def calculate_all_metrics(graph: Graph, output_dir: str):
    
    print("Calculando métricas globais...")
    global_order = graph.get_order()
    global_size = graph.get_size()
    global_density = calculate_density(global_order, global_size)
    
    global_metrics = {
        "ordem": global_order,
        "tamanho": global_size,
        "densidade": round(global_density, 6)
    }
    with open(f"{output_dir}/recife_global.json", 'w', encoding='utf-8') as f:
        json.dump(global_metrics, f, indent=4, ensure_ascii=False)
    print(f"Salvo em {output_dir}/recife_global.json")

   
    print("\nCalculando métricas por microrregião...")
    microrregioes_metrics = []
    
    
    micros = {}
    for bairro, attrs in graph.nodes_attr.items():
        microrregiao = attrs.get('microrregiao', 'N/A')
        if microrregiao not in micros:
            micros[microrregiao] = []
        micros[microrregiao].append(bairro)

    for mr_id, bairros in sorted(micros.items()):
        subgraph = graph.criar_subrafo(bairros)
        order = subgraph.get_order()
        size = subgraph.get_size()
        density = calculate_density(order, size)
        
        microrregioes_metrics.append({
            "microrregiao": mr_id,
            "ordem": order,
            "tamanho": size,
            "densidade": round(density, 6)
        })

    with open(f"{output_dir}/microrregioes.json", 'w', encoding='utf-8') as f:
        json.dump(microrregioes_metrics, f, indent=4, ensure_ascii=False)
    print(f"Salvo em {output_dir}/microrregioes.json")
    
   
    print("\nCalculando métricas de ego-rede...")
    ego_metrics = []
    for bairro in sorted(graph.adj.keys()):
        vizinhos = graph.get_neighbors(bairro)
       
        ego_nodes = {bairro} | set(vizinhos)
        
        ego_subgraph = graph.criar_subrafo(ego_nodes)
        
        ego_metrics.append({
            "bairro": bairro,
            "grau": len(vizinhos),
            "ordem_ego": ego_subgraph.get_order(),
            "tamanho_ego": ego_subgraph.get_size(),
            "densidade_ego": round(calculate_density(ego_subgraph.get_order(), ego_subgraph.get_size()), 6)
        })

    ego_df = pd.DataFrame(ego_metrics)
    ego_df.to_csv(f"{output_dir}/ego_bairro.csv", index=False, encoding='utf-8')
    print(f"Salvo em {output_dir}/ego_bairro.csv")

def calculate_degrees_and_rankings(graph: Graph, output_dir: str):
    """
    Calcula graus e rankings dos bairros:
    - Lista de graus: out/graus.csv → bairro, grau
    - Bairro mais denso: maior densidade_ego
    - Bairro com maior grau: argmax grau
    """
    print("\nCalculando graus e rankings...")
    
    # Calcular graus de todos os bairros
    graus_data = []
    for bairro in sorted(graph.adj.keys()):
        grau = len(graph.get_neighbors(bairro))
        graus_data.append({
            "bairro": bairro,
            "grau": grau
        })
    
    # Salvar lista de graus
    graus_df = pd.DataFrame(graus_data)
    graus_df.to_csv(f"{output_dir}/graus.csv", index=False, encoding='utf-8')
    print(f"Lista de graus salva em {output_dir}/graus.csv")
    
    # Ler dados de ego-rede para encontrar bairro mais denso
    ego_path = f"{output_dir}/ego_bairro.csv"
    import os
    if not os.path.exists(ego_path):
        print("Erro: Arquivo ego_bairro.csv não encontrado. Execute calculate-metrics primeiro.")
        return
    
    ego_df = pd.read_csv(ego_path)
    
    # Encontrar bairro com maior densidade_ego
    max_densidade = ego_df['densidade_ego'].max()
    bairro_mais_denso = ego_df[ego_df['densidade_ego'] == max_densidade].iloc[0]
    
    # Encontrar bairro com maior grau
    max_grau = graus_df['grau'].max()
    bairro_maior_grau = graus_df[graus_df['grau'] == max_grau].iloc[0]
    
    print("\n=== RANKINGS ===")
    print(f"Bairro mais denso (maior densidade_ego): {bairro_mais_denso['bairro'].title()}")
    print(f"  - Densidade ego: {bairro_mais_denso['densidade_ego']:.6f}")
    print(f"  - Grau: {bairro_mais_denso['grau']}")
    
    print(f"\nBairro com maior grau: {bairro_maior_grau['bairro'].title()}")
    print(f"  - Grau: {bairro_maior_grau['grau']}")
    
    # Salvar ranking summary
    ranking_summary = {
        "bairro_mais_denso": {
            "bairro": str(bairro_mais_denso['bairro']),
            "densidade_ego": float(bairro_mais_denso['densidade_ego']),
            "grau": int(bairro_mais_denso['grau'])
        },
        "bairro_maior_grau": {
            "bairro": str(bairro_maior_grau['bairro']),
            "grau": int(bairro_maior_grau['grau'])
        }
    }
    
    import json
    with open(f"{output_dir}/rankings.json", 'w', encoding='utf-8') as f:
        json.dump(ranking_summary, f, indent=4, ensure_ascii=False)
    print(f"Resumo dos rankings salvo em {output_dir}/rankings.json")
