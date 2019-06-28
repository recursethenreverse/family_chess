from abc import ABC,abstractmethod

MBL = 7 #0 index maximum board length
SIDE_WHITE = "W"
SIDE_BLACK = "B"

PIECE_PAWN = "P"
PIECE_ROOK = "R"

class Space(ABC):
    def __init__(self, x, y, **kwargs):
        self._x = -1
        self._y = -1
        self.x = x 
        self.y = y 
        self.xy = (x,y)

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,val):
        if self.check_bounds(val):
            self._x = val 
        else:
            raise ValueError("x out of bounds: {}".format(val))

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self,val):
        if self.check_bounds(val):
            self._y = val 
        else:
            raise ValueError("y is out of bounds: {}".format(val))

    def check_bounds(self,v):
        return True if 0<=v<=MBL else False 

    def check_bounds_tuple(self,xy):
        return self.check_bounds(xy[0]) and self.check_bounds(xy[1])
        
        
    def __eq__(self, value):
        return (self.x == value.x) and (self.y == value.y)

    @abstractmethod
    def __repr__(self):
        return super().__repr__()


class Square(Space):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, **kwargs)
        self.id = "{}{}".format(x,y)
        self.piece = None 

    def __repr__(self):
        if self.piece:
            return str(self.piece)
        else:
            return "[]"
            # return "{}{}".format(self.x,self.y)


class Piece(Space):
    def __init__(self, x, y, side, piece_type, **kwargs):
        self.piece_type = piece_type 
        self.side = side 
        super().__init__(x, y, **kwargs)

    @abstractmethod
    def possible_moves(self):
        pass

    @abstractmethod
    def possible_attacks(self):
        pass

    def _filter_out_of_bounds_moves(self,move_collection):
        return set([m for m in move_collection if self.check_bounds_tuple(m)])
         
    def __repr__(self):
        return "{}{}".format(self.side,self.piece_type)


class Pawn(Piece):
    def __init__(self, x, y, side, **kwargs):
        return super().__init__(x, y, side, PIECE_PAWN, **kwargs)   

    def possible_moves(self):
        base_moves = set([(self.x,self.y+1)])
        if self.y == 1: #first move can move twice
            base_moves.add((self.x,self.y+2))
        return self._filter_out_of_bounds_moves(base_moves)

    def possible_attacks(self):
        base_attacks = set([(self.x-1,self.y+1),(self.x+1,self.y+1)])
        return self._filter_out_of_bounds_moves(base_attacks)


class Rook(Piece):
    def __init__(self, x, y, side, **kwargs):
        return super().__init__(x, y, side, PIECE_ROOK, **kwargs)

    def possible_moves(self):
        x = set([(x,self.y) for x in range(MBL+1)])
        y = set([(self.x,y) for y in range(MBL+1)])
        ret = (x | y)
        ret.remove((self.x,self.y))
        return ret 
        
    def possible_attacks(self):
        return self.possible_moves()


class Board(object):
    def __init__(self, *args, **kwargs):
        self.board = []
        self.perspective = None 
        self.build_board()
        #set up pieces and reset perspective 
        self.set_up_pieces()
        self.switch_sides()
        self.set_up_pieces()
        self.switch_sides()


    def build_board(self):
        self.perspective = SIDE_WHITE
        for y in range(MBL+1):
            row = []
            self.board.append([Square(x,y) for x in range(MBL+1)] )

    def add_piece(self, piece):
        self.board[piece.y][piece.x] = piece

    def get_piece(self, xy):
        return self.board[xy[1]][xy[0]]

    def remove_piece(self, piece):
        self.board[piece.y][piece.x] = Square(piece.x, piece.y)

    def move_piece(self,piece,xy):
        p = self.get_piece(piece.xy)
        self.remove_piece(piece)
        p.x = xy[0]
        p.y = xy[1]
        self.add_piece(p)

    def set_up_pieces(self):
        #pawns
        for x in range(MBL+1):
            self.add_piece(Pawn(x,1,self.perspective))
        #rooks
        self.add_piece(Rook(0,0,self.perspective))
        self.add_piece(Rook(7,0,self.perspective))

    def switch_sides(self):
        self.board.reverse()
        [r.reverse() for r in self.board]
        self.perspective = SIDE_BLACK if self.perspective == SIDE_WHITE else SIDE_WHITE

    def print_board_to_console(self):
        print()
        print("         {}".format("black" if self.perspective == SIDE_WHITE else "white"))
        for y in range(MBL, -1, -1):
            print(" ".join([str(self.board[y][x]) for x in range(MBL+1)]))
        print("         {}".format("white" if self.perspective == SIDE_WHITE else "Black"))
        print()

class Player(object):
    def __init__(self, board, side, **kwargs):
        self.board = board 
        self.side = side 
        
    def make_move(self):
        if self.is_my_move():
            #move something here 

            b.switch_sides()

    def is_my_move(self):
        return self.board.perspective == self.side #is it my turn?
        

if __name__ == "__main__":
    b = Board()
    b.print_board_to_console()
    def move_pawns():
        for x in range(MBL+1):
            p = b.get_piece((x,1))
            if x%2:
                b.move_piece(p,max(p.possible_moves()))
            else:
                b.move_piece(p,min(p.possible_moves()))
    move_pawns()
    b.switch_sides()
    move_pawns()
    b.switch_sides()
    # p1 = b.get_piece((0,1))
    # b.move_piece(p1,max(p1.possible_moves()))
    b.print_board_to_console()
    print()