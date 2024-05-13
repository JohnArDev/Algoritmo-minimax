import math
from os import system
import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3,3), dtype=int)
        self.suma = 0

    def printState(self):
        symbols = {0: ' ', 1: 'X', -1: 'O'}
        for row in self.board:
            print("|".join(symbols[val] for val in row))

    def player(self):
        self.suma = np.sum(self.board)
        if np.sum(self.board) == 0:
            return 'X'
        else:
            return 'O'

    def actions(self):
        player = self.player()
        actions_state = []

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    action = np.zeros((3,3), dtype=int)
                    action[i][j] = 1 if player == 'X' else -1
                    actions_state.append(action)

        return actions_state

    def result(self, action):
        new_state = TicTacToe()
        new_state.board = np.add(self.board, action)
        return new_state

    def terminal(self):
        # Verificar filas y columnas
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                return True

        # Verificar diagonales
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return True

        # Verificar si la grilla está llena
        for row in self.board:
            if 0 in row:
                return False
        return True

    def utilidad(self):
        for i in range(3):
            # Verificar filas
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                return self.board[i][0]
            # Verificar columnas
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                return self.board[0][i]

        # Verificar diagonales
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[0][2]

        # Si la grilla está llena, el juego termina en empate
        return 0

    def maxValue(self):
        if self.terminal():
            return self.utilidad()
        v = -math.inf
        for action in self.actions():
            v=max(v, self.result(action).minValue())
        return v

    def minValue(self):
        if self.terminal():
            return self.utilidad()
        v = math.inf
        for action in self.actions():
            v=min(v, self.result(action).maxValue())
        return v

    def mejor_accion(self):
        acciones = self.actions()
        best_value = math.inf
        best_action = None

        for action in acciones:
            value = self.result(action).minValue()
            # print(value)
            if value < best_value:
                best_action = action
                best_value = value            

        return best_action


def juego():
    game = TicTacToe()
    while not game.terminal(): # Repetira si no esta en un estado terminal
        game.printState()
        print(f"Es el turno del jugador {game.player()}")

        if game.player() == 'X':
            while True:
                try:
                    state_game = np.zeros((3,3), dtype=int)
                    row = int(input("Ingrese la fila (1-3): ")) - 1
                    col = int(input("Ingrese la columna (1-3): ")) - 1
                    state_game[row][col] = 1
                    if np.any(np.all(state_game == game.actions(), axis=(1,2))):
                        break
                    else:
                        print("Movimiento inválido. Intente de nuevo.")
                except ValueError:
                    print("Entrada inválida. Intente de nuevo.")
            action = state_game
        else:
            action = game.mejor_accion()

        game = game.result(action)

    # Determina que ya finalizo la partida
    game.printState()
    winner = game.utilidad()
    if winner == 0:
        print("¡Empate!")
    else:
        print(f"¡El ganador es el jugador {winner}!")

    if input('Desea reiniciar el juego? s/n: ') == 's':
        system("cls")
        juego()

if __name__ == "__main__":
    juego()