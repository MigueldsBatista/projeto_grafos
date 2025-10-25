import pandas as pd
from typing import List, Dict, Set, Iterable
        
type NomeVertice = str

class Vertice:
    def __init__(self, nome: NomeVertice):
        self.nome = nome
        self.vizinhos: List[Vertice] = []
         # como vamos representar pesos??
    
    def adicionar_vizinho(self, vizinho: 'Vertice') -> bool:
        reusltado = False
        if vizinho not in self.vizinhos:
            self.vizinhos.append(vizinho)
            self.vizinhos.sort()
            reusltado = True
        return reusltado
    
    def tem_adjagencia(self, vertice: 'Vertice'):
        return vertice in self.vizinhos

class Graph:
    vertices: Dict[NomeVertice, Vertice] = {}

    def pertence_ao_grafo(self, vertice: Vertice) -> bool:
        return vertice.nome in self.vertices

    def adicionar_vertice(self, vertice: Vertice) -> bool:
        reusltado = False
        vertice_tem_tipo_correto = isinstance(vertice, Vertice)
        vertice_nao_visitado = vertice.nome not in self.vertices

        if (vertice_tem_tipo_correto and vertice_nao_visitado):
            self.vertices.update({ vertice.nome: vertice })
            reusltado = True
        return reusltado
    
    def adicionar_aresta(self, verticeA: Vertice, verticeB: Vertice) -> bool:
        resultado = False
        if self.pertence_ao_grafo(verticeA) and self.pertence_ao_grafo(verticeB):
            self.vertices.get(verticeA.nome).adicionar_vizinho(verticeB)
            self.vertices.get(verticeB.nome).adicionar_vizinho(verticeA)
            resultado = True
        return resultado

    def criar_subrafo(self, vertices_para_incluir: Iterable[Vertice]) -> 'Graph':
        subgrafo = Graph()
        vertices = set(vertices_para_incluir)
        
        for vertice in vertices:
            if vertice in self.nodes_attr:
                subgrafo.add_node(vertice, self.nodes_attr[vertice])
        
       
        # for node in node_set:
        #     if node in self.nodes_attr:
        #         subgraph.add_node(node, self.nodes_attr[node])
        
       
        # for u in subgraph.adj:
           
        #     if u in self.adj:
        #         for v in self.adj[u]:
                    
        #             if v in subgraph.adj:
        #                 subgraph.add_edge(u, v)
        
        # return subgraph
        
    @property
    def ordem(self) -> int:
        return len(self.adj)

    @property
    def tamanho(self) -> int:
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2

    def __str__(self) -> str:
        linhas = []
        for key in sorted(self.vertices.keys()):
            vizinhos = [v.nome for v in self.vertices[key].vizinhos]
            linhas.append(f"{key}: {vizinhos}")
        return "\n".join(linhas)


def load_from_csv(self, nodes_path: str, edges_path: str):
    
    nodes_df = pd.read_csv(nodes_path)
    for _, row in nodes_df.iterrows():
        self.add_node(row['bairro'], {'microrregiao': str(row['microrregiao'])})

    
    edges_df = pd.read_csv(edges_path)
    for _, row in edges_df.iterrows():
        self.add_edge(row['bairro_origem'], row['bairro_destino'])