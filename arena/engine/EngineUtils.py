import chess

from Piece import Piece

pieceTypes = {'R': 'rook', 'N': 'knight', 'K': 'king', 'Q': 'queen', 'B': 'bishop', 'P': 'pawn'}


def getInitialPieces():
    pieces = []
    pieces.extend(__getWhitePieces())
    pieces.extend(__getBlackPieces())
    return pieces


def __getWhitePieces():
    pieces = []
    for i in range(8):
        pieces.append(Piece("white", i, 6, "pawn"))
    pieces.append(Piece("white", 5, 7, "bishop"))
    pieces.append(Piece("white", 2, 7, "bishop"))
    pieces.append(Piece("white", 0, 7, "rook"))
    pieces.append(Piece("white", 7, 7, "rook"))
    pieces.append(Piece("white", 1, 7, "knight"))
    pieces.append(Piece("white", 6, 7, "knight"))
    pieces.append(Piece("white", 4, 7, "king"))
    pieces.append(Piece("white", 3, 7, "queen"))
    return pieces


def __getBlackPieces():
    pieces = []
    for i in range(8):
        pieces.append(Piece("black", i, 1, "pawn"))
    pieces.append(Piece("black", 5, 0, "bishop"))
    pieces.append(Piece("black", 2, 0, "bishop"))
    pieces.append(Piece("black", 0, 0, "rook"))
    pieces.append(Piece("black", 7, 0, "rook"))
    pieces.append(Piece("black", 1, 0, "knight"))
    pieces.append(Piece("black", 6, 0, "knight"))
    pieces.append(Piece("black", 3, 0, "king"))
    pieces.append(Piece("black", 4, 0, "queen"))
    return pieces



def getPieceFrom(coordinates: float, piece: str):
    color = "white"
    if piece.islower() is True:
        color = "black"
    x = coordinates % 8
    y = coordinates // 8

    return Piece(color, x, y, pieceTypes[piece.upper()])

##TODO: Not perfectly precise but good enough and I'm tired of playing with pixels
def getMoveFromPos(pos: tuple):
    xRaw = pos[0]
    x = (xRaw // 122)

    yRaw = pos[1]
    y = ((yRaw // 122) - 7) * -1

    return chess.square(x,y)
