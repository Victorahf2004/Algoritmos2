import matplotlib.pyplot as plt

class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def coords(self):
        return f'CoordX: {self.x} CoordY: {self.y}'

class Vector:
    def __init__(self, pInicio, pFinal):
        self.pInicio = pInicio
        self.pFinal = pFinal
        self.a1 = pFinal.x - pInicio.x
        self.a2 = pFinal.y - pInicio.y
    
    def imprimirPontos(self):
        print(f'Ponto de início: {self.pInicio.coords()}')
        print(f'Ponto final: {self.pFinal.coords()}')
        print(f'Componentes a1:{self.a1}, a2:{self.a2}')
        print(f'Vetor: ({self.a1}, {self.a2})')

class Plano:
    def __init__(self):
        self.vetores = []
    
    def adicionarVetor(self, vetor):
        self.vetores.append(vetor)
    
    def plotPlano(self):
        plt.figure(figsize=(8, 6))
        contador = 0
        for vetor in self.vetores:
            plt.plot([vetor.pInicio.x, vetor.pFinal.x], [vetor.pInicio.y, vetor.pFinal.y], marker='o')
            plt.text(vetor.pInicio.x, vetor.pInicio.y, 'Inicio')
            plt.text(vetor.pFinal.x, vetor.pFinal.y, f'vetor[{contador}]')
            contador +=1
        
        plt.xlabel('Coordenada X')
        plt.ylabel('Coordenada Y')
        plt.title('Representação de Vetores no Plano')
        plt.grid(True)
        plt.show()

def magnitudeVetorial(vetor1, vetor2):
    a1 = vetor1.a1
    a2 = vetor1.a2
    b1 = vetor2.a1
    b2 = vetor2.a2
    a1b2 = a1 * b2
    b1a2 = b1 * a2
    c = a1b2 - b1a2
    if c > 0:
        print('a está numa posição horária de b')
    elif c < 0:
        print('a está numa posição anti-horária de b')
    else:
        print('a e b são colineares')

def mudancaDirecao3Pontos(p0, p1, p2):
    vet1 = Vector(p0, p1)
    vet2 = Vector(p0, p2)
    a1 = vet1.a1
    a2 = vet1.a2
    b1 = vet2.a1
    b2 = vet2.a2
    a1b2 = a1 * b2
    b1a2 = b1 * a2
    c = a1b2 - b1a2
    direcao = ''
    if c > 0:
        direcao = 'horario'
        print('Seguindo p0, p1, p2, tem sentido horário')
    elif c < 0:
        direcao = 'anti-horário'
        print('Seguindo p0, p1, p2, tem sentido anti-horário')
    else:
        direcao = 'colinear'
        print('P0, p1 e p2 são colineares')
    plt.figure(figsize=(8, 6))
    contador = 0
    vetores = [vet1, vet2]
    contador = 0
    for vetor in vetores:
        plt.plot([vetor.pInicio.x, vetor.pFinal.x], [vetor.pInicio.y, vetor.pFinal.y], marker='o')
        plt.text(vetor.pInicio.x, vetor.pInicio.y, 'Inicio')
        plt.text(vetor.pFinal.x, vetor.pFinal.y, f'vetor[{contador}]')
        contador +=1
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Representação de Vetores no Plano')
    plt.grid(True)
    plt.show()
    return direcao
plano = Plano()

p1 = Ponto(0, 0)
p2 = Ponto(-1, 4)
p3 = Ponto(1, 4)
mudancaDirecao3Pontos(p3, p1, p2)
# v1 = Vector(p1, p2)
# v1.imprimirPontos()
# plano.adicionarVetor(v1)

# p3 = Ponto(0, 0)
# p4 = Ponto(1, 4)
# v2 = Vector(p3, p4)
# v2.imprimirPontos()
# plano.adicionarVetor(v2)
# magnitudeVetorial(v2, v1)
# plano.plotPlano()