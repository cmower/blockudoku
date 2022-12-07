import sys
from game import Game
from agent import Human

Agent = Human
# Agent = AI

def main():
    Game(sys.argv, Agent()).spin()

if __name__ == '__main__':
    main()
