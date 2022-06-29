class move_set():

    def __init__(self):
        pass

    def processBoard(self, FEN):
        board = []
        rights = []
        tempboard = []
        spcases = FEN.split(" ")
        for i in spcases[0:1]:
            tempboard.append(i)
        for i in spcases[1:]:
            rights.append(i)
        tempboard = tempboard[0].split("/")
        n = 9
        index = 0
        while(index < 65):
            for s in tempboard:
                n-=1
                letters = ["a","b","c","d","e","f","g","h"]
                lcount = 0
                row = []
                for i in range (len(s)):
                    letter = s[i:i+1]
                    if letter.isdigit():
                        for i in range (int(letter)):
                            row.append((letters[lcount]+str(n), "0"))
                            lcount+=1
                            index+=1
                    else:
                        row.append((letters[lcount]+str(n), letter))
                        lcount+=1
                        index+=1
                board.append(row)
        return board, rights


    def allPossibleMoves(self, board, row, col, rights):
        moveList = []
        if board[row][col][1] == "p" or board[row][col][1] == "P":
            moveList = self.PawnMoves(board, row, col, rights)
        elif board[row][col][1] == "K" or board[row][col][1] == "k":
            moveList = self.KingMoves(board, row, col, rights)
        elif board[row][col][1] == "Q" or board[row][col][1] == "q":
            moveList = self.QueenMoves(board, row, col)
        elif board[row][col][1] == "B" or board[row][col][1] == "b":
            moveList = self.BishopMoves(board, row, col)
        elif board[row][col][1] == "R" or board[row][col][1] == "r":
            moveList = self.RookMoves(board, row, col, rights)
        elif board[row][col][1] == "N" or board[row][col][1] == "n":
            moveList = self.KnightMoves(board, row, col)
        else:
            moveList = []
        return moveList   

    def PawnMoves(self, board, row, col, rights):
        piece = board[row][col][1]
        team = "black"
        if board[row][col][1] == "P":
            team = "white"
        moveList = []
        r, c = row+1, col-1
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team == "black" and tempteam == "white":
            moveList.append(piece+board[row][col][0] + " to "+ piece + board[r][c][0])
        r, c, = row+1, col+1
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team == "black" and tempteam == "white":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
        r, c, = row-1, col+1
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team == "white" and tempteam == "black":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
        r, c, = row-1, col-1
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team == "white" and tempteam == "black":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row-1][col-1][0])
        r, c, = row-1, col
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team == "white" and tempteam == "blank":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row-1][col][0])
        r, c, = row+1, col
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team == "black" and tempteam == "blank":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row+1][col][0])
        r, c, = row+2, col
        tempteam = self.checkTeam(board, r, c)
        tempteam2 = self.checkTeam(board, r-1, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team == "black" and tempteam == "blank" and row == 1 and tempteam2 == "blank":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0] +"ep")
        r, c, = row-2, col
        tempteam = self.checkTeam(board, r, c)
        tempteam2 = self.checkTeam(board, row+1, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team == "white" and tempteam == "blank" and row == 6 and tempteam2 == "blank":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0] + "ep")
        #enpassant
        if rights[1] != "-":
            epchart = self.get_row_and_col(rights[1])
            if team == "black" and epchart[0] == 5:
                if (row == epchart[0]-1 and col == epchart[1]-1) or (row == epchart[0]-1 and col == epchart[1]+1):
                    moveList.append(piece+board[row][col][0] + " to "+rights[1])
            if team == "white" and epchart[0] == 2:
                if (row == epchart[0]+1 and col == epchart[1]-1) or (row == epchart[0]+1 and col == epchart[1]+1):
                    moveList.append(piece+board[row][col][0] + " to "+rights[1])
        return moveList

    def KingMoves(self, board, row, col, rights):
        piece = board[row][col][1]
        team = "black"
        if board[row][col][1] == "K":
            team = "white"
        moveList = []
        r, c, = row-1, col-1
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row-1][col-1][0])
        r, c, = row+1, col+1
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row+1][col+1][0])
        r, c, = row-1, col+1
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row-1][col+1][0])
        r, c, = row+1, col-1
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row+1][col-1][0])
        r, c, = row, col-1
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row][col-1][0])
        r, c, = row, col+1
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row][col+1][0])
        r, c, = row-1, col
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row-1][col][0])
        r, c, = row+1, col
        tempteam = self.checkTeam(board, r, c)
        if r <= 8 and r >= 0 and c <= 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row+1][col][0])
        return moveList

    def QueenMoves(self, board, row, col):
        piece = board[row][col][1]
        team = "black"
        if board[row][col][1] == "Q":
            team = "white"
        moveList = []
        r, c = row+1, col+1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r+=1; c+=1
        r, c = row-1, col-1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank" or team == tempteam:
                c = 100; r = 100
            r-=1; c-=1
        r, c = row+1, col-1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r+=1; c-=1
        r, c = row-1, col+1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r-=1; c+=1
        r, c = row, col+1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            c+=1
        r, c = row, col-1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            c-=1
        r, c = row+1, col
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r+=1
        r, c = row-1, col
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r-=1
        return moveList

    def BishopMoves(self, board, row, col):
        moveList = []
        piece = board[row][col][1]
        team = "black"
        if board[row][col][1] == "B":
            team = "white"
        r, c = row+1, col+1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r+=1; c+=1
        r, c = row-1, col-1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r-=1; c-=1
        r, c = row+1, col-1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r+=1; c-=1
        r, c = row-1, col+1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r-=1; c+=1
        return moveList

    def RookMoves(self, board, row, col, rights):
        piece = board[row][col][1]
        team = "black"
        if board[row][col][1] == "R":
            team = "white"
        moveList = []
        r, c = row, col+1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            c+=1
        r, c = row, col-1
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            c-=1
        r, c = row+1, col
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r+=1
        r, c = row-1, col
        while r < 8 and r >= 0 and c < 8 and c >= 0:
            tempteam = self.checkTeam(board,r,c)
            if team != tempteam:
                moveList.append(piece+board[row][col][0] + " to "+piece + board[r][c][0])
            if team != tempteam and tempteam != "blank"or team == tempteam:
                c = 100; r = 100
            r-=1

        return moveList

    def KnightMoves(self, board, row, col): 
        piece = board[row][col][1]
        team = "black"
        if board[row][col][1] == "N":
            team = "white"
        moveList = []
        r, c, = row-2, col-1
        tempteam = self.checkTeam(board, r, c)
        if r < 8 and r >= 0 and c < 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row-2][col-1][0])

        r, c  = row-2, col+1 
        tempteam = self.checkTeam(board, r, c)
        if r < 8 and r >= 0 and c < 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row-2][col+1][0])

        r, c= row-1, col-2
        tempteam = self.checkTeam(board, r, c)
        if r < 8 and r >= 0 and c < 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row-1][col-2][0])

        r, c = row-1, col+2
        tempteam = self.checkTeam(board, r, c)
        if r < 8 and r >= 0 and c < 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row-1][col+2][0])

        r, c = row+1, col+2
        tempteam = self.checkTeam(board, r, c)
        if r < 8 and r >= 0 and c < 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row+1][col+2][0])

        r, c = row+1, col-2
        tempteam = self.checkTeam(board, r, c)
        if r < 8 and r >= 0 and c < 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row+1][col-2][0])

        r, c = row+2, col-1
        tempteam = self.checkTeam(board, r, c)
        if r < 8 and r >= 0 and c < 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row+2][col-1][0])

        r, c = row+2, col+1
        tempteam = self.checkTeam(board, r, c)
        if r < 8 and r >= 0 and c < 8 and c >= 0 and team != tempteam and tempteam != "notvalid":
            moveList.append(piece+board[row][col][0] + " to "+piece + board[row+2][col+1][0])

        return moveList

    def checkTeam(self, board, row, col):
        if row < 8 and row >= 0 and col < 8 and col >= 0:
            if board[row][col][1] == "0":
                return "blank"
            team = "white"
            if board[row][col][1].islower():
                team = "black"
            return team
        else:
            return "notvalid"

    def printBoard(self, board):
        for r in range(8):
            for c in range(8):
                if board[r][c][1] == "0":
                    print(".", end = " ")
                else:
                    print(board[r][c][1], end = " ")
            print()

    def whiteThreatMap(self, board, rights): # what white is threatening
        WTM = set()
        for r in range(0,8):
            moves = []
            for c in range(0,8):
                if (not board[r][c][1].isdigit()) and board[r][c][1].isupper(): 
                    moves = self.allPossibleMoves(board, r, c, rights)
            if len(moves) > 0:
                for m in moves:
                    WTM.add(m[7:])
        return WTM

    def blackThreatMap(self, board, rights): # what black is threatening
        BTM = set()
        for r in range(0,8):
            moves = []
            for c in range(0,8):
                if (not board[r][c][1].isdigit()) and board[r][c][1].islower(): 
                    moves = self.allPossibleMoves(board, r, c, rights)
            if len(moves) > 0:
                for m in moves:
                    BTM.add(m[7:])
        return BTM

    def canCastle(self, board, r, c, rights):
        piece = board[r][c][1]
        if "Q" in rights[2]:
            BTM = self.blackThreatMap(board, rights)
            if piece == "R":
                if self.checkSpots(board, 7, 0, "queenside", BTM):
                    return piece+board[r][c][0] + " to "+piece + board[7][3][0], "Q"
            if piece == "K":
                if self.checkSpots(board, 7, 0, "queenside", BTM):
                    return piece+board[r][c][0] + " to "+piece + board[7][1][0], "Q"         
        if "q" in rights[2]:
            WTM = self.whiteThreatMap(board, rights)
            if piece == "r":
                if self.checkSpots(board, 0, 0, "queenside", WTM):
                    return piece+board[r][c][0] + " to "+piece + board[0][3][0], "q"
            if piece == "k":
                if self.checkSpots(board, 0, 0, "queenside", WTM):
                    return piece+board[r][c][0] + " to "+piece + board[0][1][0], "q"
        if "K" in rights[2]:
            BTM = self.blackThreatMap(board, rights)
            if piece == "R":
                if self.checkSpots(board, 7, 4, "kingside", BTM):
                    return piece+board[r][c][0] + " to "+piece + board[7][5][0], "K"
            if piece == "K":
                if self.checkSpots(board, 7, 4, "kingside", BTM):
                    return piece+board[r][c][0] + " to "+piece + board[7][6][0], "K"
        if "k" in rights[2]:
            WTM = self.whiteThreatMap(board, rights)
            if piece == "r": 
                if self.checkSpots(board, 0, 4, "kingside", WTM):
                    return piece+board[r][c][0] + " to "+piece + board[0][5][0], "k"
            if piece == "k":
                if self.checkSpots(board, 0, 4, "kingside", WTM):
                    return piece+board[r][c][0] + " to "+piece + board[0][6][0], "k"
        return "nocastle", "nocastle"

    def checkSpots(self, board, sr, sc, side, TM):
        if side == "queenside":
            if not board[sr][sc+1][0] in TM and board[sr][sc+1][1] == "0":
                if not board[sr][sc+2][0] in TM and board[sr][sc+2][1] == "0":
                    if not board[sr][sc+3][0] in TM and board[sr][sc+3][1] == "0":
                        return True
        else:
            if not board[sr][sc+1][0] in TM and board[sr][sc+1][1] == "0":
                if not board[sr][sc+2][0] in TM and board[sr][sc+2][1] == "0":
                        return True
        return False

    def get_row_and_col(self, spot):
        letters = ["a","b","c","d","e","f","g","h"]
        lcount = 0
        ncount = 8
        matrix = {}
        for r in range(0, 8):
            for c in range(0, 8):
                matrix.update({letters[lcount]+str(ncount):[r,c]})
                lcount += 1
            lcount = 0
            ncount -= 1
        return matrix.get(spot)

    def get_TM(self, team, FEN):
        board, rights = self.processBoard(FEN)
        if team == "black":
            threatmap = self.whiteThreatMap(board, rights)
            return threatmap
        else:
            threatmap = self.blackThreatMap(board, rights)
            return threatmap

    def process_move(self, FEN):
        board, rights = self.processBoard(FEN)
        team = rights[0]
        if rights[0] == "w":
            team = "white"
        else:
            team = "black"
        moveset = set()
        kr, kc = -1,-1
        for r in range(0,8):
            moves = []
            for c in range(0,8):
                if(not board[r][c][1].isdigit()) and self.checkTeam(board, r, c) == team:
                    moves = self.allPossibleMoves(board, r, c, rights)
                if board[r][c][1] == "R" or board[r][c][1] == "r" or board[r][c][1] == "K" or board[r][c][1] == "k":
                    move, castle = self.canCastle(board, r, c, rights)
                    if move != "nocastle":
                        moves.append(move)
                if((board[r][c][1] == "K" and self.checkTeam(board, r, c) == team) or (board[r][c][1] == "k" and self.checkTeam(board, r, c) == team)):
                    kr, kc = r,c
                for m in moves:
                    moveset.add(m)
            count = 0
            for m in moveset:
                count+=1
                tempboard, newrights = self.processBoard(FEN)
                piece, location = m[7:8], m[8:10]
                r,c = self.get_row_and_col(location)
                tempboard[r][c] = (location, piece)
                threatmap = self.get_TM(team, FEN)
                if board[kr][kc][0] in threatmap:
                    moveset.remove(m)
        return moveset, count, castle
    '''
    def simulate_move(self, move, FEN):
        newfen = self.update_fen(FEN, move)
        newlist = self.process_move(newfen)
        return newlist, newfen
    '''


    def update_fen(self, FEN, currentmove):
        board, rights = self.processBoard(FEN)
        moves, count, castle = self.process_move(FEN)
        piece, location = currentmove[7:8], currentmove[8:10]
        r,c = self.get_row_and_col(location)
        board[r][c] = (location, piece)
        newrow = ""
        count = 0
        for col in range(0,8):
            letter = board[r][col][1]
            if letter == "0":
                count+=1
            else:
                if count > 0:
                    newrow += str(count)
                count=0
                newrow += board[r][col][1]
        if count > 0:
            newrow+= str(count)
        index, index1, index2, count = 0,0,0,0
        temp = FEN
        while count <= r:
            if not "/" in temp:
                index = temp.index(" ")
            else:
                index = temp.index("/")
            index1+=index
            temp = temp[index+1:]
            if not "/" in temp:
                index = temp.index(" ")
            else:
                index = temp.index("/")
            index2 = index + index1
            count+=1
        index1+=count-1
        index2+=count
        FEN1, FEN2 = FEN[0:index1+1], FEN[index2:]
        FEN = FEN1 + newrow + FEN2
        piece, location = "0", currentmove[1:3]
        r,c = self.get_row_and_col(location)
        board[r][c] = (location, "0")
        newrow = ""
        count = 0
        for col in range(0,8):
            letter = board[r][col][1]
            if letter == "0":
                count+=1
            else:
                if count > 0:
                    newrow += str(count)
                count=0
                newrow += board[r][col][1]
        if count > 0:
            newrow+= str(count)
        index, index1, index2, count = 0,0,0,0
        temp = FEN
        while count <= r:
            if not "/" in temp:
                index = temp.index(" ")
            else:
                index = temp.index("/")
            index1+=index
            temp = temp[index+1:]
            if not "/" in temp:
                index = temp.index(" ")
            else:
                index = temp.index("/")
            index2 = index + index1
            count+=1
        index1+=count-1
        index2+=count
        FEN1, FEN2 = FEN[0:index1+1], FEN[index2:]
        FEN = FEN1 + newrow + FEN2
        if rights[0] == "w":
            rights[0] = "b"
        else:
            rights[0] = "w"
            rights[4] = str(int(rights[4])+1)
        rights[3] = str(int(rights[3])+1)
        if castle != "nocastle":
            rights[2] = rights[2].replace(castle, "")
        if "ep" in currentmove:
            rights[1] = location
        tempboard = FEN.split(" ")
        FEN = tempboard[0] + " " + rights[0]+" "+rights[1]+" "+rights[2]+" "+rights[3]+" "+rights[4]
        board2, rights2 = self.processBoard(FEN)
        newmovelistt, count, castle = self.process_move(FEN)
        return FEN, newmovelistt
   

#FEN = "rnb1k3/pppp1p2/4pn2/8/3NP3/2N4q/PPP2PP1/R1B1KB2 w - Qq 0 13"
#Game = move_set()





















    
    
       

        












