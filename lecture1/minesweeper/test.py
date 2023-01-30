import minesweeper as ms

if __name__ == "__main__":
    
    newGame = ms.MinesweeperAI()

    newGame.add_knowledge((3,3),4)

    print(newGame.knowledge)
    newGame.show_knowledge
