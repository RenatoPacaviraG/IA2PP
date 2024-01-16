import random
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

class Agente:
    def __init__(self, nome, posicao):
        self.nome = nome
        self.posicao = posicao
        self.forte = False

def criar_tabuleiro(tamanho):
    return [['L' for _ in range(tamanho)] for _ in range(tamanho)]

def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(' '.join(map(str, linha)))
    print()

def definir_cenario_manual(tabuleiro):
    num_bombas = int(input("Digite o número de bombas: "))
    num_tesouros = int(input("Digite o número de tesouros: "))
    num_agentes = int(input("Digite o número de agentes: "))

    preencher_bombas_e_tesouros(tabuleiro, num_bombas, num_tesouros)
    posicionar_agentes(tabuleiro, num_agentes)

def preencher_aleatoriamente(tabuleiro):
    tamanho = len(tabuleiro)
    num_bombas = random.randint(1, tamanho * tamanho // 3)
    num_tesouros = random.randint(1, tamanho * tamanho // 3)
    num_agentes = random.randint(1, tamanho * tamanho // 5)

    preencher_bombas_e_tesouros(tabuleiro, num_bombas, num_tesouros)
    posicionar_agentes(tabuleiro, num_agentes)

def preencher_bombas_e_tesouros(tabuleiro, num_bombas, num_tesouros):
    tamanho = len(tabuleiro)

    # Preencher Bombas
    for _ in range(num_bombas):
        linha, coluna = random.randint(0, tamanho-1), random.randint(0, tamanho-1)
        while tabuleiro[linha][coluna] != 'L':
            linha, coluna = random.randint(0, tamanho-1), random.randint(0, tamanho-1)
        tabuleiro[linha][coluna] = 'B'

    # Preencher Tesouros
    for _ in range(num_tesouros):
        linha, coluna = random.randint(0, tamanho-1), random.randint(0, tamanho-1)
        while tabuleiro[linha][coluna] != 'L':
            linha, coluna = random.randint(0, tamanho-1), random.randint(0, tamanho-1)
        tabuleiro[linha][coluna] = 'T'

def posicionar_agentes(tabuleiro, num_agentes):
    tamanho = len(tabuleiro)
    agentes = []

    for i in range(num_agentes):
        linha, coluna = random.randint(0, tamanho-1), random.randint(0, tamanho-1)
        while tabuleiro[linha][coluna] != 'L':
            linha, coluna = random.randint(0, tamanho-1), random.randint(0, tamanho-1)

        agente = Agente(f"Agente-{i+1}", (linha, coluna))
        agentes.append(agente)
        tabuleiro[linha][coluna] = f"A-{i+1}"

def obter_posicoes_bombas_desativadas(agentes):
    return set(agente.posicao for agente in agentes if agente.forte)

def treinar_modelo_knn(bombas_desativadas):
    X = np.array(list(bombas_desativadas))
    y = np.ones(len(X))  # Todas as posições contêm bombas
    knn_model = KNeighborsClassifier(n_neighbors=1)
    knn_model.fit(X, y)
    return knn_model

def prever_bomba(knn_model, posicao):
    return knn_model.predict([posicao])[0]

def mover_agentes(tabuleiro, agentes, bombas_desativadas, knn_model):
    for agente in agentes:
        linha, coluna = agente.posicao

        if tabuleiro[linha][coluna] == 'B' and not agente.forte:
            if not prever_bomba(knn_model, (linha, coluna)):
                print(f"{agente.nome} foi destruído por uma Bomba!")
                agentes.remove(agente)
            else:
                print(f"{agente.nome} desativou uma Bomba!")
                bombas_desativadas.add((linha, coluna))
        elif tabuleiro[linha][coluna] == 'T':
            print(f"{agente.nome} ficou forte!")
            agente.forte = True
        else:
            tabuleiro[linha][coluna] = 'L'
            nova_linha, nova_coluna = linha - 1, coluna
            if 0 <= nova_linha < len(tabuleiro) and tabuleiro[nova_linha][nova_coluna] == 'L':
                tabuleiro[nova_linha][nova_coluna] = f"A-{agente.nome}"

            # Restaurar a posição anterior do agente
            tabuleiro[linha][coluna] = f"A-{agente.nome}"

def main():
    tamanho = 10
    tabuleiro = criar_tabuleiro(tamanho)
    agentes = []
    bombas_desativadas = set()

    while True:
        print("Escolha uma opção:")
        print("1 - Definir o número de Bombas, Tesouros e Agentes no tabuleiro")
        print("2 - Preencher aleatoriamente com Bombas, Tesouros e Agentes")
        print("3 - Treinar modelo KNN")
        print("4 - Mover agentes")
        print("5 - Sair")

        opcao = input("Opção: ")

        if opcao == '1':
            definir_cenario_manual(tabuleiro)
            imprimir_tabuleiro(tabuleiro)
            agentes = [agente for linha in tabuleiro for agente in linha if isinstance(agente, Agente)]
        elif opcao == '2':
            preencher_aleatoriamente(tabuleiro)
            imprimir_tabuleiro(tabuleiro)
            agentes = [agente for linha in tabuleiro for agente in linha if isinstance(agente, Agente)]
        elif opcao == '3':
            bombas_desativadas = obter_posicoes_bombas_desativadas(agentes)
            knn_model = treinar_modelo_knn(bombas_desativadas)
            print("Modelo KNN treinado.")
        elif opcao == '4':
            if not agentes:
                print("Não há agentes no tabuleiro. Crie agentes primeiro.")
            elif not bombas_desativadas:
                print("Não há bombas desativadas. Treine o modelo KNN primeiro.")
            else:
                mover_agentes(tabuleiro, agentes, bombas_desativadas, knn_model)
                imprimir_tabuleiro(tabuleiro)
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
