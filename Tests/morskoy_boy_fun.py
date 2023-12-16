def restore_used_blocks(deleted_ship, used_blocks_set):
    for block in deleted_ship:
        for i in range(-1, 2):
            for j in range(-1, 2):
                used_blocks_set.discard((block[0]+i, block[1]+j))
    return used_blocks_set


def update_used_blocks(ship, used_blocks_set):
    for block in ship:
        for i in range(-1, 2):
            for j in range(-1, 2):
                used_blocks_set.add((block[0]+i, block[1]+j))
    return used_blocks_set


def ship_is_valid(ship_set, blocks_for_manual_drawing):
    return ship_set.isdisjoint(blocks_for_manual_drawing)


def check_ships_numbers(ship, num_ship_list):
    return (5 - len(ship)) > num_ship_list[len(ship) - 1]


def update_dotted_and_hit_sets(fired_block, player2_turn, diagonal_only=True):
    global dotted_set
    x, y = fired_block
    a, b = 0, 11
    if not player2_turn:
        a += 15
        b += 15
    hit_blocks.add((x, y))
    for i in range(-1, 2):
        for j in range(-1, 2):
            if diagonal_only:
                if i != 0 and j != 0 and a < x + i < b and 0 < y + j < 11:
                    dotted_set.add((x+i, y+j))
            else:
                if a < x + i < b and 0 < y + j < 11:
                    dotted_set.add((x+i, y+j))
    dotted_set -= hit_blocks


def add_missed_block_to_dotted_set(fired_block):
    dotted_set.add(fired_block)


def update_destroyed_ships(ind, player2_turn, opponents_ships_list_original_copy):
    ship = sorted(opponents_ships_list_original_copy[ind])
    for i in range(-1, 1):
        update_dotted_and_hit_sets(ship[i], player2_turn, False)


dotted_set = set()
hit_blocks = set()
