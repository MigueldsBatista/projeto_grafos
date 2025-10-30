import pandas as pd
from typing import List, Dict, Set, Iterable, Union
        
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
    
    def adicionar_vizinhos(self, vizinhos: List['Vertice']):
        [self.adicionar_vizinho(vizinho) for vizinho in vizinhos]
    
    def remover_vizinho(self, vizinho: 'Vertice'):
        resultado = False
        if vizinho in self.vizinhos:
            self.vizinhos.remove(vizinho)
            resultado = True
        return resultado
    
    def remover_vizinhos(self, vizinhos: List['Vertice']):
        [self.remover_vizinho(vizinho) for vizinho in vizinhos]

    def limpar_vizinhos(self):
        self.vizinhos.clear()

    def tem_adjagencia(self, vertice: 'Vertice'):
        return vertice in self.vizinhos
    
    def __str__(self):
        return self.nome
    

class Grafo:
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

    def criar_subrafo(self, vertices_para_incluir: Iterable[Union[Vertice, str]]) -> 'Grafo':
        subgrafo = Grafo()
        
        nomes_vertices_incluidos = {str(v) for v in vertices_para_incluir}

        for nome in nomes_vertices_incluidos:
            subgrafo.adicionar_vertice(Vertice(nome))

        for nome in nomes_vertices_incluidos:
            vertice_original = self.vertices.get(nome)
            
            if not vertice_original:
                continue

            for vertice_vizinho in vertice_original.vizinhos:
                if vertice_vizinho.nome in nomes_vertices_incluidos:
                    subgrafo.adicionar_aresta(
                        subgrafo.vertices.get(nome),
                        subgrafo.vertices.get(vertice_vizinho.nome)
                    )

        return subgrafo

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

