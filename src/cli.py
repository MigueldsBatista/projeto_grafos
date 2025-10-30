# 5. Pasta /src/
# Código principal dividido por responsabilidade:
# Gerencia os argumentos de linha de comando (--dataset, --alg, --source, --target, --out)
# Chama as funções certas do solve.py



import argparse
import os
from graphs.io import process_bairros_data, normalize_text
from graphs.graph import Grafo
from solve import calculate_all_metrics, calculate_degrees_and_rankings
"""
    comandos para rodar esse script:
    1.python src/cli.py process-nodes: PROCESSA OS DADOS DOS BAIRROS
    2.python src/cli.py build-graph : VE A ORDEM E TAMANHO DO GRAFO
    3.python src/cli.py calculate-metrics : CALCULA AS METRICAS
"""
import pandas as pd

def load_from_csv(self, nodes_path: str, edges_path: str):
    
    nodes_df = pd.read_csv(nodes_path)

    for _, row in nodes_df.iterrows():
        self.add_node(row['bairro'], {'microrregiao': str(row['microrregiao'])})

    
    edges_df = pd.read_csv(edges_path)
    for _, row in edges_df.iterrows():
        self.add_edge(row['bairro_origem'], row['bairro_destino'])


def _get_base_dir():
    
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _load_graph() -> Grafo:
    
    base_dir = _get_base_dir()
    nodes_path = os.path.join(base_dir, 'data', 'bairros_unique.csv')
    edges_path = os.path.join(base_dir, 'data', 'adjacencias_bairros.csv')
    
    if not os.path.exists(nodes_path) or not os.path.exists(edges_path):
        raise FileNotFoundError(
        "Arquivos de dados não encontrados. Execute 'process-nodes' e certifique-se que 'adjacencias_bairros.csv' existe."
        )

    g = Grafo()
    load_from_csv(nodes_path, edges_path)
    
    return g

def handle_process_nodes(args):
   
    base_dir = _get_base_dir()
    input_path = os.path.join(base_dir, 'data', 'bairros_recife.csv')
    output_path = os.path.join(base_dir, 'data', 'bairros_unique.csv')
    
    try:
        process_bairros_data(input_path, output_path)
        print(f"Processamento concluído. Nós salvos em: {output_path}")
    except Exception as e:
        print(f"Erro ao processar nós: {e}")

def handle_build_graph(args):
    
    try:
        g = _load_graph()
        print(g)

        if args.neighbors:
            bairro_normalizado = normalize_text(args.neighbors)
            if bairro_normalizado in g.adj:
                vizinhos = g.get_neighbors(bairro_normalizado)
                print(f"\nVizinhos de '{args.neighbors}': {', '.join(v.title() for v in vizinhos)}")
            else:
                print(f"\nErro: Bairro '{args.neighbors}' não encontrado no grafo.")
    except Exception as e:
        print(f"Erro ao construir o grafo: {e}")

def handle_calculate_metrics(args):
   
    try:
        print("Carregando o grafo para cálculo de métricas...")
        g = _load_graph()
        output_dir = os.path.join(_get_base_dir(), 'out')
        os.makedirs(output_dir, exist_ok=True)
        
        calculate_all_metrics(g, output_dir)
        print("\nCálculo de métricas concluído com sucesso!")
    except Exception as e:
        print(f"Erro ao calcular métricas: {e}")

def handle_degrees_rankings(_):##passo 4 calculo de graus e rankings
    """
    Calcula graus e rankings dos bairros
    """
    try:
        print("Carregando o grafo para cálculo de graus e rankings...")
        g = _load_graph()
        output_dir = os.path.join(_get_base_dir(), 'out')
        os.makedirs(output_dir, exist_ok=True)
        
        calculate_degrees_and_rankings(g, output_dir)
        print("\nCálculo de graus e rankings concluído com sucesso!")
    except Exception as e:
        print(f"Erro ao calcular graus e rankings: {e}")

def main():
   
    parser = argparse.ArgumentParser(description="Análise de Grafos do Recife")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Comandos disponíveis")

    
    parser_process = subparsers.add_parser("process-nodes", help="Processa o CSV de bairros para criar a lista de nós.")
    parser_process.set_defaults(func=handle_process_nodes)
    
    
    parser_build = subparsers.add_parser("build-graph", help="Constrói o grafo e exibe informações sobre ele.")
    parser_build.add_argument("--neighbors", type=str, help="Exibe os vizinhos do bairro especificado.")
    parser_build.set_defaults(func=handle_build_graph)

    
    parser_metrics = subparsers.add_parser("calculate-metrics", help="Calcula métricas globais, por microrregião e de ego-redes.")
    parser_metrics.set_defaults(func=handle_calculate_metrics)

    
    parser_degrees = subparsers.add_parser("degrees-rankings", help="Calcula graus e rankings dos bairros.")
    parser_degrees.set_defaults(func=handle_degrees_rankings)

    args = parser.parse_args()
    args.func(args)

    # python3 src/cli.py process-nodes
    # python3 src/cli.py build-graph --neighbors "Boa Viagem"
    # python3 src/cli.py calculate-metrics
    # python3 src/cli.py degrees-rankings

if __name__ == "__main__":
    main()