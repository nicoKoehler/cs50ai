import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count


    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells): return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if self.count == 0: return self.cells



    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells:
            self.cells = self.cells - cell
            self.count -= 1
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        if cell in self.cells:
            self.cells = self.cells - set(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        self.moves_made.add(cell)
        self.mark_safe(cell)
        self.knowledge.append(Sentence({cell}, 0))

        #add safe cells separately, otherwise it would need to be popped out and returned later
        neighbours = self.find_neighbour_cells(cell)
        if neighbours and len(neighbours) >= count: 
            self.knowledge.append(Sentence(neighbours, count))
        elif neighbours and len(neighbours) < count: 
            #there cannot be more mines than there are neighbours
            raise ValueError

        
        
        #once a change has occured, the loop needs to run again to see if the new knowledge created can be deducted
        newKnowledge = True

        while newKnowledge:
            newKnowledge = False 
            #sort, so it only has to traverse nxn/2, instead of n x n
            knowledge_sorted = sorted(self.knowledge, key=lambda x: len(x.cells))

            for m, sentence_from in enumerate(knowledge_sorted):
                for sentence_to in knowledge_sorted[m+1:]:

                    if sentence_from.cells.issubset(sentence_to.cells) and sentence_from.count < sentence_to.count: 
                        
                        cells_new = sentence_to.cells - sentence_from.cells
                        count_new = sentence_to.count - sentence_from.count
                        sentence_new = Sentence(cells_new, count_new)

                        #since its a set, repeated sentences could also be added. But the while loop would run infinite in this case, hence the condition
                        if sentence_new not in self.knowledge: 
                            self.knowledge.append(Sentence(cells_new, count_new))
                            newKnowledge = True
                        
                        if count_new == 0 and len(cells_new) > 0:
                            for c in cells_new:
                                self.mark_safe(c)
                        
                        elif count_new == len(cells_new) and len(cells_new) > 0:
                            for c in cells_new:
                                self.mark_mine(c)

            if not newKnowledge: break



    def show_knowledge(self, knowledge=[]):
        print("---Knowledge---")
        if not knowledge: knowledge=self.knowledge
        knowledge_sorted = sorted(knowledge, key = lambda x: len(x.cells))
        for i,k in enumerate(knowledge):
            print(f"{i}: {{{k}}}")

        print("---fin---")





    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        possibleMoves = []

        for m in self.safes:
            if m not in self.moves_made and m not in self.mines:
                possibleMoves.append[m]
        
        if possibleMoves: return possibleMoves[0]
        return None



    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        while True: 
            possibleMove = (random.randint(0,self.height-1),random.randint(0, self.width-1))
            possibleMovesChecked = set()
            
            #catch all to avoid endless loop
            if len(possibleMovesChecked) == (self.height * self.width):
                print("no moves found")
                return None

            if possibleMove not in self.moves_made and possibleMove not in self.mines and possibleMove not in possibleMovesChecked:
                return possibleMove

            possibleMovesChecked.add(possibleMove)


    def find_neighbour_cells(self, cell):
        """
        Returns a set of all neighbouring cells for a given cell, within bounds of the board
        """
        neighbours = set()
        
    
        for i in range(-1, 2):
            for j in range(-1,2):
                if 0 <= (cell[0] +i) < self.height and 0 <= (cell[1] + j) < self.width and ((cell[0]+i, cell[1]+j) != cell):
                    neighbours.add((cell[0]+i, cell[1]+j))

                

        return neighbours


    
