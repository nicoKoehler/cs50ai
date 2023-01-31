import minesweeper as ms

if __name__ == "__main__":
    
    newGame = ms.MinesweeperAI()

    newGame.add_knowledge((3,3),3)
    newGame.show_knowledge()
    newGame.add_knowledge((4,4),2)
    newGame.show_knowledge()
