import unittest
from morskoy_boy_fun import *


class MyTestCase(unittest.TestCase):
    def test_update_used_blocks(self):
        ship = {(3, 3)}
        used_blocks_set = {(1, 1), (2, 2)}
        updated_set = update_used_blocks(ship, used_blocks_set)
        self.assertEqual(updated_set, {(4, 4), (2, 4), (3, 4), (4, 3),
                                       (1, 1), (4, 2), (2, 3), (3, 3), (2, 2), (3, 2)})

        ship = {(3, 3), (2, 5)}
        used_blocks_set = {(4, 5), (5, 2), (12, 4)}
        updated_set = update_used_blocks(ship, used_blocks_set)
        self.assertNotEqual(updated_set, {(3, 4), (16, 6), (16, 8), (18, 8)})

    def test_restore_used_blocks(self):
        deleted_ship = [(3, 3)]
        used_blocks_set = {(1, 1), (2, 2), (3, 3)}
        restored_set = restore_used_blocks(deleted_ship, used_blocks_set)
        self.assertEqual(restored_set, {(1, 1)})

        deleted_ship = [(1, 6), (5, 12)]
        used_blocks_set = {(1, 5), (2, 2), (3, 3), (3, 4), (16, 6), (16, 8), (18, 8)}
        restored_set = restore_used_blocks(deleted_ship, used_blocks_set)
        self.assertNotEqual(restored_set, {(6, 4), (10, 6), (13, 8), (12, 8), (5, 9)})

    def test_ship_is_valid(self):
        ship_set = {(1, 2), (3, 4), (5, 6)}
        blocks_for_manual_drawing = {(7, 8), (9, 10)}
        self.assertEqual(ship_is_valid(ship_set, blocks_for_manual_drawing), True)

        ship_set = {(1, 2), (3, 4), (5, 6)}
        blocks_for_manual_drawing = {(5, 6), (7, 8), (9, 10)}
        self.assertEqual(ship_is_valid(ship_set, blocks_for_manual_drawing), False)

    def test_check_ships_numbers(self):
        ship = [(1, 2), (1, 3), (1, 4)]
        num_ship_list = [3, 1, 1, 1]
        self.assertEqual(check_ships_numbers(ship, num_ship_list), True)

        ship = [(1, 2), (3, 4), (5, 6), (7, 8)]
        num_ship_list = [2, 3, 0, 1]
        self.assertEqual(check_ships_numbers(ship, num_ship_list), False)

    def test_update_dotted_and_hit_sets(self):  # {(3, 4), (16, 6), (18, 6), (16, 8), (18, 8), (5, 2)}
        dotted_set = {(5, 2), (3, 4)}
        hit_blocks = {(17, 6)}
        fired_block = (17, 7)
        player2_turn = False
        update_dotted_and_hit_sets(fired_block, player2_turn)
        self.assertNotEqual(dotted_set, {(3, 4), (16, 6), (16, 8), (18, 8)})

    def test_add_missed_block_to_dotted_set(self):
        fired_block = (3, 4)
        add_missed_block_to_dotted_set(fired_block)
        self.assertEqual(dotted_set, {(3, 4)})

    def test_update_destroyed_ships(self):
        ind = 0
        player2_turn = True
        opponents_ships_list_original_copy = [[(4, 5), (5, 5), (6, 5)], [(2, 3), (2, 4)]]
        update_destroyed_ships(ind, player2_turn, opponents_ships_list_original_copy)
        assert (6, 6) in dotted_set
        assert (7, 6) in dotted_set
        self.assertEqual(len(dotted_set), 13)


if __name__ == '__main__':
    unittest.main()
