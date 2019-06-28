import unittest
from chess_engine import Board, Square, Space, Piece, Pawn, Rook, Bishop
from chess_engine import MBL,PIECE_PAWN,SIDE_BLACK



class Test_Board(unittest.TestCase):
    def test_build_board(self):
        b = Board()
        self.assertEqual(len(b.board),MBL+1)

    def test_add_piece(self):
        b = Board()
        p = Pawn(0,1,SIDE_BLACK)
        b.add_piece(p)
        self.assertEqual(b.board[p.y][p.x],p)
        b.remove_piece(p)
        self.assertEqual(b.board[p.y][p.x],Square(p.x,p.y))

    def test_remove_piece(self):
        b = Board()
        p = Pawn(0,1,SIDE_BLACK)
        b.add_piece(p)
        self.assertEqual(b.board[p.y][p.x],p)
        b.remove_piece(p)


class Test_Space(unittest.TestCase):
    def test_abc(self):
        with self.assertRaises(TypeError):
            s = Space(0,0)
    def test_bounds(self):
        s = Space
        self.assertTrue(s.check_bounds(None,0))
        self.assertTrue(s.check_bounds(None,7))
        self.assertFalse(s.check_bounds(None,-1))
        self.assertFalse(s.check_bounds(None,8))




class Test_Square(unittest.TestCase):
    def test_repr(self):
        s = Square(0,0)
        self.assertEqual(str(s), "[]")

    def test_base_class_checkbounds(self):
        s = Square(0,0)
        self.assertTrue(s.check_bounds(0))
        self.assertTrue(s.check_bounds(7))
        self.assertFalse(s.check_bounds(-1))
        self.assertFalse(s.check_bounds(8))

class Test_Piece(unittest.TestCase):
    def test_abc(self):
        with self.assertRaises(TypeError):
             p = Piece(0,0,SIDE_BLACK,PIECE_PAWN)

class Test_Pawn(unittest.TestCase):
    def test_repr(self):
        p = Pawn(0,0,SIDE_BLACK)
        self.assertEqual(str(p),"BP")

    def test_possible_moves(self):
        p = Pawn(0,2,SIDE_BLACK)
        self.assertEqual(p.possible_moves(),set([(0,3)]))
        p = Pawn(0,1,SIDE_BLACK)
        self.assertEqual(p.possible_moves(),set([(0,2),(0,3)]))
        p = Pawn(0,MBL,SIDE_BLACK)
        self.assertEqual(p.possible_moves(),set([]))

    def test_possible_attacks(self):
        p = Pawn(0,2,SIDE_BLACK)
        self.assertEqual(p.possible_attacks(),set([(1,3)]))

        p = Pawn(1,1,SIDE_BLACK)
        self.assertEqual(p.possible_attacks(),set([(0,2),(2,2)]))

        p = Pawn(0,MBL,SIDE_BLACK)
        self.assertEqual(p.possible_attacks(),set([]))

class Test_Rook(unittest.TestCase):
    def test_possible_moves(self):
        r = Rook(0,0,SIDE_BLACK)
        expected_results = set([(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)])
        self.assertEqual(r.possible_moves(),expected_results)

    def test_possible_attacks(self):
        r = Rook(4,4,SIDE_BLACK)
        expected_results = set([(4,0),(0,4),(4,1),(4,2),(4,3),(4,5),(4,6),(4,7),(1,4),(2,4),(3,4),(5,4),(6,4),(7,4)])
        self.assertEqual(r.possible_moves(),expected_results)


class Test_Bishop(unittest.TestCase):
    def test_possible_moves(self):
        b = Bishop(5,5,SIDE_BLACK)
        expected_results = set([(0,0),(1,1),(2,2),(3,3),(4,4),(6,6),(7,7),(4,6),(3,7),(6,4),(7,3)])
        self.assertEqual(b.possible_moves(),expected_results) 

    def test_possible_attacks(self):
        b = Bishop(0,0,SIDE_BLACK)
        expected_results = set([(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)])
        self.assertEqual(b.possible_moves(),expected_results) 
        

if __name__ == "__main__":
    unittest.main()