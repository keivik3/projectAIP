import pygame
import random
import copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_BLUE = (0, 153, 153)
LIGHT_GRAY = (192, 192, 192)
RED = (255, 0, 0)

block_size = 50
left_margin = 2 * block_size
upper_margin = block_size

size = (left_margin+30*block_size, upper_margin+15*block_size)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
dotted_set = set()
hit_blocks = set()
destroyed_ships_list = []
pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Morskoy Boy")

font_size = int(block_size / 1.5)

font = pygame.font.SysFont('notosans', font_size)


class AutoShips:
    def __init__(self, offset):
        self.offset = offset
        self.available_blocks = set((x, y) for x in range(1+self.offset, 11+self.offset) for y in range(1, 11))
        self.ships_set = set()
        self.ships = self.populate_grid()

    def create_start_block(self, available_blocks):
        x_or_y = random.randint(0, 1)
        str_rev = random.choice((-1, 1))
        x, y = random.choice(tuple(available_blocks))
        return x, y, x_or_y, str_rev

    def create_ship(self, number_of_blocks, available_blocks):
        ship_coordinates = []
        x, y, x_or_y, str_rev = self.create_start_block(available_blocks)
        for _ in range(number_of_blocks):
            ship_coordinates.append((x, y))
            if not x_or_y:
                str_rev, x = self.get_new_block_to_ship(
                    x, str_rev, x_or_y, ship_coordinates)
            else:
                str_rev, y = self.get_new_block_to_ship(
                    y, str_rev, x_or_y, ship_coordinates)
        if self.is_ship_valid(ship_coordinates):
            return ship_coordinates
        return self.create_ship(number_of_blocks, available_blocks)

    def get_new_block_to_ship(self, coor, str_rev, x_or_y, ship_coordinates):
        if (coor <= 1 - self.offset*(x_or_y-1) and str_rev == -1) or (
                coor >= 10 - self.offset*(x_or_y-1) and str_rev == 1):
            str_rev *= -1
            return str_rev, ship_coordinates[0][x_or_y] + str_rev
        else:
            return str_rev, ship_coordinates[-1][x_or_y] + str_rev

    def is_ship_valid(self, new_ship):
        ship = set(new_ship)
        return ship.issubset(self.available_blocks)

    def add_new_ship_to_set(self, new_ship):
        self.ships_set.update(new_ship)

    def update_available_blocks_for_creating_ships(self, new_ship):
        for elem in new_ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if 0+self.offset < (elem[0]+k) < 11+self.offset and 0 < (elem[1]+m) < 11:
                        self.available_blocks.discard((elem[0]+k, elem[1]+m))

    def populate_grid(self):
        ships_coordinates_list = []
        for number_of_blocks in range(4, 0, -1):
            for _ in range(5-number_of_blocks):
                new_ship = self.create_ship(
                    number_of_blocks, self.available_blocks)
                ships_coordinates_list.append(new_ship)
                self.add_new_ship_to_set(new_ship)
                self.update_available_blocks_for_creating_ships(new_ship)
        return ships_coordinates_list


class Button:
    def __init__(self, x_offset, button_title, message_to_show):
        self.title = button_title
        self.title_width, self.title_height = font.size(self.title)
        self.message = message_to_show
        self.button_width = self.title_width + block_size
        self.button_height = self.title_height + block_size
        self.x_start = x_offset
        self.y_start = upper_margin + 10 * block_size + self.button_height
        self.rect_for_draw = self.x_start, self.y_start, self.button_width, self.button_height

        self.rect = pygame.Rect(self.rect_for_draw)

        self.rect_for_draw_button_title = (self.x_start + self.button_width / 2 - self.title_width / 2,
                                           self.y_start + self.button_height / 2 - self.title_height / 2)
        self.color = BLACK

    def draw_button(self, color=None):
        if not color:
            color = self.color
        pygame.draw.rect(screen, color, self.rect_for_draw)
        text_to_blit = font.render(self.title, True, WHITE)
        screen.blit(text_to_blit, self.rect_for_draw_button_title)

    def change_color_on_hover(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.draw_button(GREEN_BLUE)

    def print_message_for_button(self):
        if self.message:
            message_width, message_height = font.size(self.message)
            rect_for_message = (self.x_start / 2 - message_width / 2,
                                self.y_start + self.button_height / 2 - message_height / 2)
            text = font.render(self.message, True, BLACK)
            screen.blit(text, rect_for_message)


player2 = AutoShips(15)
# player1_ships_working = copy.deepcopy(player1.ships)
player2_ships_working = copy.deepcopy(player2.ships)

auto_button_place = left_margin + 17 * block_size
manual_button_place = left_margin + 20 * block_size
how_to_create_ships_message = "Как вы хотите создать корабли? Нажмите кнопку"
auto_button = Button(auto_button_place, "АВТО", how_to_create_ships_message)
manual_button = Button(manual_button_place, "ВРУЧНУЮ", how_to_create_ships_message)
undo_message = "Для отмены последнего корабля нажмити кнопку"
undo_button_place = left_margin + 14 * block_size
undo_button = Button(undo_button_place, "ОТМЕНА", undo_message)
message_rect_for_drawing_ships = (undo_button.rect_for_draw[0] + undo_button.rect_for_draw[2],
                                  upper_margin + 11 * block_size,
                                  size[0] - (undo_button.rect_for_draw[0] + undo_button.rect_for_draw[2]), 4*block_size)
player1_ships_to_draw = []


def draw_ships(ships_coordinates_list):
    for elem in ships_coordinates_list:
        ship = sorted(elem)
        x_start = ship[0][0]
        y_start = ship[0][1]
        # Hor and 1block ships
        ship_width = block_size * len(ship)
        ship_height = block_size
        # Vert ships
        if len(ship) > 1 and ship[0][0] == ship[1][0]:
            ship_width, ship_height = ship_height, ship_width
        x = block_size * (x_start - 1) + left_margin
        y = block_size * (y_start - 1) + upper_margin
        pygame.draw.rect(
            screen, BLACK, ((x, y), (ship_width, ship_height)), width=block_size//10)


class Grid:
    """
        Class to draw the grids and add title, numbers and letters to them

        :param title:  Players' name
        :type title: str
        :param offset: Where the grid starts
        :type offset: int

        """
    def __init__(self, title, offset):
        self.title = title
        self.offset = offset
        self.draw_grid()
        self.add_nums_letters_to_grid()
        self.sign_grids()

    def draw_grid(self):
        for i in range(11):
            # Hor grid
            pygame.draw.line(screen, BLACK, (left_margin+self.offset, upper_margin+i*block_size),
                             (left_margin+10*block_size+self.offset, upper_margin+i*block_size), 1)
            # Vert grid
            pygame.draw.line(screen, BLACK, (left_margin+i*block_size+self.offset, upper_margin),
                             (left_margin+i*block_size+self.offset, upper_margin+10*block_size), 1)

    def add_nums_letters_to_grid(self):
        for i in range(10):
            num_ver = font.render(str(i+1), True, BLACK)
            letters_hor = font.render(LETTERS[i], True, BLACK)
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            # Ver num grid1
            screen.blit(num_ver, (left_margin - (block_size//2+num_ver_width//2)+self.offset,
                                  upper_margin + i*block_size + (block_size//2 - num_ver_height//2)))
            # Hor LETTERS grid1
            screen.blit(letters_hor, (left_margin + i*block_size + (block_size //
                                                                    2 - letters_hor_width//2)+self.offset,
                                      upper_margin - block_size))

    def sign_grids(self):
        player = font.render(self.title, True, BLACK)
        sign_width = player.get_width()
        screen.blit(player, (left_margin + 5 * block_size - sign_width // 2 + self.offset,
                             upper_margin - block_size // 2 - font_size + 11 * block_size))


def check_hit_or_miss(fired_block, opponents_ships_list, player2_turn, opponents_ships_list_original_copy,
                      opponents_ships_set):
    for elem in opponents_ships_list:
        diagonal_only = True
        if fired_block in elem:
            # This is to put dots before and after a destroyed ship
            # and to draw computer's destroyed ships (which are hidden until destroyed)
            ind = opponents_ships_list.index(elem)
            if len(elem) == 1:
                diagonal_only = False
            update_dotted_and_hit_sets(
                fired_block, player2_turn, diagonal_only)
            elem.remove(fired_block)
            # This is to check who loses - if ships_set is empty
            opponents_ships_set.discard(fired_block)
            if not elem:
                update_destroyed_ships(
                    ind, player2_turn, opponents_ships_list_original_copy)
            if not player2_turn:
                return False
            else:
                return True
    add_missed_block_to_dotted_set(fired_block)
    if player2_turn:
        return False
    else:
        return True


def add_missed_block_to_dotted_set(fired_block):
    dotted_set.add(fired_block)


def update_destroyed_ships(ind, player2_turn, opponents_ships_list_original_copy):
    ship = sorted(opponents_ships_list_original_copy[ind])
    for i in range(-1, 1):
        update_dotted_and_hit_sets(ship[i], player2_turn, False)


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


def draw_from_dotted_set(dotted_set):
    for elem in dotted_set:
        pygame.draw.circle(screen, BLACK, (block_size*(
            elem[0]-0.5)+left_margin, block_size*(elem[1]-0.5)+upper_margin), block_size//6)


def draw_hit_blocks(hit_blocks):
    for block in hit_blocks:
        x1 = block_size * (block[0]-1) + left_margin
        y1 = block_size * (block[1]-1) + upper_margin
        pygame.draw.line(screen, BLACK, (x1, y1),
                         (x1+block_size, y1+block_size), block_size//6)
        pygame.draw.line(screen, BLACK, (x1, y1+block_size),
                         (x1+block_size, y1), block_size//6)


def show_message_at_rect_center(text, rect, which_font=font, color=RED):
    text_width, text_height = which_font.size(text)
    text_rect = pygame.Rect(rect)
    x_start = text_rect.centerx - text_width / 2
    y_start = text_rect.centery - text_height / 2
    background_rect = pygame.Rect(x_start - block_size / 2, y_start, text_width + block_size, text_height)
    text_to_blit = which_font.render(text, True, color)
    screen.fill(WHITE, background_rect)
    screen.blit(text_to_blit, (x_start, y_start))


def ship_is_valid(ship_set, blocks_for_manual_drawing):
    return ship_set.isdisjoint(blocks_for_manual_drawing)


def check_ships_numbers(ship, num_ship_list):
    return (5 - len(ship)) > num_ship_list[len(ship) - 1]


def update_used_blocks(ship, used_blocks_set):
    for block in ship:
        for i in range(-1, 2):
            for j in range(-1, 2):
                used_blocks_set.add((block[0]+i, block[1]+j))
    return used_blocks_set


def restore_used_blocks(deleted_ship, used_blocks_set):
    for block in deleted_ship:
        for i in range(-1, 2):
            for j in range(-1, 2):
                used_blocks_set.discard((block[0]+i, block[1]+j))
    return used_blocks_set


def main():
    game_over = False
    player2_turn = False
    screen.fill(WHITE)
    drawing = False
    start = (0, 0)
    ship_size = (0, 0)
    ships_creation_not_decided = True
    ships_not_created = True
    rect_for_grids = (0, 0, size[0], upper_margin + 12 * block_size)
    rect_for_messages_and_buttons = (0, upper_margin + 11 * block_size, size[0], 5 * block_size)
    player1_ships_to_draw = []
    player1_ships_set = set()
    used_blocks_for_manual_drawing = set()
    num_ships_list = [0, 0, 0, 0]
    player1_grid = Grid("PLAYER1", 0)
    player2_grid = Grid("PLAYER2", 15 * block_size)
    # draw_ships(player1.ships)
    # draw_ships(player2.ships)
    pygame.display.update()

    while ships_creation_not_decided:
        auto_button.draw_button()
        manual_button.draw_button()
        auto_button.change_color_on_hover()
        manual_button.change_color_on_hover()
        auto_button.print_message_for_button()

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                ships_creation_not_decided = False
                ships_not_created = False
            # If AUTO button is pressed - create human ships automatically
            elif event.type == pygame.MOUSEBUTTONDOWN and auto_button.rect.collidepoint(mouse):
                print("Clicked AUTO!", event.pos)
                player1 = AutoShips(0)
                player1_ships_to_draw = player1.ships
                player1_ships_set = player1.ships_set
                player1_ships_working = copy.deepcopy(player1.ships)
                ships_creation_not_decided = False
                ships_not_created = False
            elif event.type == pygame.MOUSEBUTTONDOWN and manual_button.rect.collidepoint(mouse):
                ships_creation_not_decided = False

        pygame.display.update()
        screen.fill(WHITE, rect_for_messages_and_buttons)

    while ships_not_created:
        screen.fill(WHITE, rect_for_grids)
        player1_grid = Grid("PLAYER1", 0)
        player2_grid = Grid("PLAYER2", 15 * block_size)
        undo_button.draw_button()
        undo_button.print_message_for_button()
        undo_button.change_color_on_hover()
        mouse = pygame.mouse.get_pos()
        if not player1_ships_to_draw:
            undo_button.draw_button(LIGHT_GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ships_not_created = False
                game_over = True
            elif undo_button.rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
                if player1_ships_to_draw:
                    deleted_ship = player1_ships_to_draw.pop()
                    num_ships_list[len(deleted_ship) - 1] -= 1
                    used_blocks_for_manual_drawing = restore_used_blocks(
                        deleted_ship, used_blocks_for_manual_drawing)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                x_start, y_start = event.pos
                start = x_start, y_start
                ship_size = (0, 0)
            elif drawing and event.type == pygame.MOUSEMOTION:
                x_end, y_end = event.pos
                end = x_end, y_end
                ship_size = x_end - x_start, y_end - y_start
            elif drawing and event.type == pygame.MOUSEBUTTONUP:
                x_end, y_end = event.pos
                drawing = False
                ship_size = (0, 0)
                start_block = ((x_start - left_margin) // block_size + 1,
                               (y_start - upper_margin) // block_size + 1)
                end_block = ((x_end - left_margin) // block_size + 1,
                             (y_end - upper_margin) // block_size + 1)
                if start_block > end_block:
                    start_block, end_block = end_block, start_block
                temp_ship = []
                if (0 < start_block[0] < 15 and 0 < start_block[1] < 11 and
                        0 < end_block[0] < 15 and 0 < end_block[1] < 11):
                    screen.fill(WHITE, message_rect_for_drawing_ships)
                    if start_block[0] == end_block[0] and (end_block[1] - start_block[1]) < 4:
                        for block in range(start_block[1], end_block[1] + 1):
                            temp_ship.append((start_block[0], block))
                    elif start_block[1] == end_block[1] and (end_block[0] - start_block[0]) < 4:
                        for block in range(start_block[0], end_block[0] + 1):
                            temp_ship.append((block, start_block[1]))
                    else:
                        show_message_at_rect_center(
                            "КОРАБЛЬ СЛИШКОМ БОЛЬШОЙ!", message_rect_for_drawing_ships)
                else:
                    show_message_at_rect_center(
                        "КОРАБЛЬ ЗА ПРЕДЕЛАМИ СЕТКИ!", message_rect_for_drawing_ships)
                if temp_ship:
                    temp_ship_set = set(temp_ship)
                    if ship_is_valid(temp_ship_set, used_blocks_for_manual_drawing):
                        if check_ships_numbers(temp_ship, num_ships_list):
                            num_ships_list[len(temp_ship) - 1] += 1
                            player1_ships_to_draw.append(temp_ship)
                            player1_ships_set |= temp_ship_set
                            used_blocks_for_manual_drawing = update_used_blocks(
                                temp_ship, used_blocks_for_manual_drawing)
                        else:
                            show_message_at_rect_center(
                                f"ДОСТАТОЧНО {len(temp_ship)}-ПАЛУБНЫХ КОРАБЛЕЙ", message_rect_for_drawing_ships)
                    else:
                        show_message_at_rect_center(
                            "КОРАБЛИ ПРИКАСАЮТСЯ!", message_rect_for_drawing_ships)
            if len(player1_ships_to_draw) == 10:
                ships_not_created = False
                player1_ships_working = copy.deepcopy(player1_ships_to_draw)
                screen.fill(WHITE, rect_for_messages_and_buttons)
        pygame.draw.rect(screen, BLACK, (start, ship_size), 3)
        draw_ships(player1_ships_to_draw)
        pygame.display.update()

    while not game_over:
        draw_ships(player1_ships_to_draw)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif not player2_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (left_margin + 15 * block_size < x < left_margin + 25 * block_size) and (
                        upper_margin < y < upper_margin + 10 * block_size):
                    fired_block = ((x - left_margin) // block_size + 1, (y - upper_margin) // block_size + 1)
                    player2_turn = check_hit_or_miss(fired_block, player2_ships_working, False,
                                                     player2.ships, player2.ships_set)
            elif player2_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (left_margin < x < left_margin + 10 * block_size) and (
                        upper_margin < y < upper_margin + 10 * block_size):
                    fired_block = ((x - left_margin) // block_size + 1, (y - upper_margin) // block_size + 1)
                    player2_turn = check_hit_or_miss(fired_block, player1_ships_working, True,
                                                     player1_ships_to_draw, player1_ships_set)
        if not player2.ships_set:
            show_message_at_rect_center(
                "ВЫИГРАЛ PlAYER1!", (0, 0, size[0], size[1]), font)
        if not player1_ships_set:
            show_message_at_rect_center(
                "ВЫИГРАЛ PLAYER2!", (0, 0, size[0], size[1]), font)
        pygame.display.update()
        draw_from_dotted_set(dotted_set)
        draw_hit_blocks(hit_blocks)
        draw_ships(destroyed_ships_list)
        pygame.display.update()


main()
pygame.quit()
