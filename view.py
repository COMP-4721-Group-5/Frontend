import sys

import pygame

from lib.shared.player import Player
from lib.frontend.Logic import Logic
from lib.shared.internal_structures import Board, Placement, Tile


def tile_img_load(tile: Tile):
    """Method for getting the images for the tile

    Args:
        tile: Tile to load to an image

    Returns: 
        The image of the tile.
    """
    if tile == 0:
        return None
    fileName = 'assets/tile_img/%s-%s.png' % (tile.color.name.lower(),
                                              tile.shape.name.lower())
    return pygame.image.load(fileName)


class View:
    """Renders view for frontend client

    Responsible for rendering the frontend view. After initialization,
    calls to render_grid(), render_hand(), and render_details() can be
    performed automatically by calling update_view(). The event loop is
    for handling basic view-related events, such as closing the window
    or dragging and dropping a tile onto the grid.

    Attributes:
        __top_left_x: The top left x offset of the board on the view compared with the board object itself
        __top_left_y: The top left y offset of the board on the view compared with the board object itself
        __frame_size: The size of the board frame displayed on the view
        __selected_tile: The currently selected tile
        __window_size: Size of the window, contains x,y
        __screen: The screen object
        __logic: Instance of the logic class that will be used to access the logic methods
        __board: Instance of the board object that will be used to interact with the board

    """

    __top_left_x: int = 108
    __top_left_y: int = 108
    __frame_size: int = 8
    __selected_tile: Tile = None
    __window_size = 0, 0
    __screen = None
    __logic: Logic = None
    __board: Board = None

    def __init__(self, size, g_logic):
        """Inits the view"""
        self.__logic = g_logic
        self.__window_size = size
        self.__screen = pygame.display.set_mode(size)
        self.__board = self.__logic.board
        favicon = pygame.image.load('favicon.png')
        pygame.display.set_icon(favicon)
        background_color = (255, 255, 255)
        pygame.display.set_caption("Qwirkle")
        self.__screen.fill(background_color)
        self.update_view()
        self.init_event_loop()

    def update_view(self):
        """Updates the entire view.

            Returns:
                Nothing
        """
        self.render_grid(self.__screen, self.__window_size, self.__top_left_x,
                         self.__top_left_y)
        self.render_hand(self.__screen, self.__window_size)
        self.render_details()
        pygame.display.flip()

    def render_grid(self, screen, window_size, top_left_x, top_left_y):
        """Renders the main grid on which tiles may be placed.

            Args:
                screen: screen object returned by pygame.display.set_mode()
                window_size: dimensions of the Qwirkle window
                top_left_x: x coordinate for top-left tile of frame
                top_left_y: y coordinate for top-left tile of frame

            Returns:
                Nothing
        """
        border_color = (0, 0, 0)
        background_color = (255, 255, 255)
        self.draw_hollow_rect(screen, background_color, border_color,
                              (0.09 * window_size[0]), (0.05 * window_size[1]),
                              (0.8 * window_size[0]), (0.8 * window_size[1]),
                              10)
        num_rows = self.__frame_size
        num_cols = self.__frame_size
        tile_width = 1 + ((0.8 * window_size[0]) - (5 * 2)) / num_rows
        tile_height = 1 + ((0.8 * window_size[1]) - (5 * 2)) / num_cols
        x_pos = (0.09 * window_size[0]) + 10
        y_pos = (0.05 * window_size[1]) + 10
        for i in range(num_rows):
            x_pos = (0.09 * window_size[0]) + 10
            for j in range(num_cols):
                self.draw_hollow_rect(screen, background_color, border_color,
                                      x_pos, y_pos, tile_width, tile_height, 5)
                curr_tile = self.__board.get_board()[self.__top_left_y + i,
                                                     self.__top_left_x + j]
                if curr_tile != 0:
                    tile_img = pygame.transform.scale(
                        tile_img_load(curr_tile),
                        (tile_width - 10, tile_height - 10))
                    screen.blit(tile_img, (x_pos + 5, y_pos + 5))
                x_pos = x_pos + tile_width - 2
            y_pos = y_pos + tile_height - 2

    def render_hand(self, screen, window_size):
        """Renders the tiles currently held by the player.

            Args:
                screen: screen object returned by pygame.display.set_mode()
                window_size: dimensions of the Qwirkle window

            Returns:
                Nothing
        """

        border_color = (0, 0, 0)
        background_color = (255, 255, 255)
        tile_width = 1 + ((0.8 * window_size[0]) - (5 * 2)) / 8
        tile_height = 1 + ((0.8 * window_size[1]) - (5 * 2)) / 8
        num_tiles = 7
        gap = 10
        x_pos = ((0.09 * window_size[0]) + 10)
        y_pos = ((0.05 * window_size[1]) + 8) + (8 * tile_height) + gap
        self.draw_hollow_rect(screen, background_color, border_color,
                              x_pos - 10, y_pos - 5, 5 + tile_width * 6,
                              tile_height + 10, 15)
        for i in range(num_tiles + 1):
            if self.__selected_tile == i:
                border_color = (255, 0, 255)
            if i < 6:
                self.draw_hollow_rect(screen, background_color, border_color,
                                      x_pos, y_pos, tile_width, tile_height, 5)
                if self.__logic.player[i] is not None:
                    curr_tile = self.__logic.player[i]
                    tile_img = pygame.transform.scale(
                        tile_img_load(curr_tile),
                        (tile_width - 10, tile_height - 10))
                    screen.blit(tile_img, (x_pos + 5, y_pos + 5))
            if i == 7:
                self.draw_hollow_rect(screen, background_color, border_color,
                                      x_pos, y_pos, tile_width, tile_height, 5)
            x_pos = x_pos + tile_width - 2
            border_color = (0, 0, 0)

    def render_details(self):
        """Renders details such as the server IP and the player's score."""
        pass

    def draw_hollow_rect(self, screen, color, border_color, x, y, width, height,
                         border_width):
        """Draws a hollow rectangle

            Args:
                screen: screen object returned by pygame.display.set_mode()
                color: the background color
                border_color: the color of the border
                x: x position of the top left corner
                y: y position of the top left corner
                width: width of the rectangle
                height: height of the rectangle
                border_width: width of the border

            Returns:
                Nothing
        """
        pygame.draw.rect(screen, border_color, pygame.Rect(x, y, width, height))
        pygame.draw.rect(
            screen, color,
            pygame.Rect(x + border_width, y + border_width,
                        width - (2 * border_width),
                        height - (2 * border_width)))

    def init_event_loop(self):
        """Event loop for handling UI interaction """
        running = True
        while (running):
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    tile_width = 90
                    gap_width = 8
                    total_width = 585
                    if (100 < x < 685) and (
                            700 < y < 770):  # Handles interaction with hand
                        relative_x = x - 100
                        for i in range(6):
                            if relative_x < (585 / 6) * (i + 1):
                                self.__selected_tile = i
                                self.update_view()
                                break
                    if (100 < x < 877) and (
                            53 < y < 667
                    ) and self.__selected_tile != 0:  # Handles interaction with the grid
                        relative_x = x - 100
                        relative_y = y - 53
                        found = False
                        for i in range(self.__frame_size):
                            if relative_x < (777 / self.__frame_size) * (i + 1):
                                for j in range(self.__frame_size):
                                    if relative_y < (
                                            615 / self.__frame_size) * (j + 1):
                                        # self.__board[self.__top_left_x + j,self.__top_left_y + i] = self.__logic.player[self.__selected_tile]
                                        placement = Placement(
                                            self.__logic.player[
                                                self.__selected_tile],
                                            self.__top_left_x + j,
                                            self.__top_left_y + i)
                                        self.__board.add_tile(placement)
                                        found = True
                                        self.update_view()
                                        break
                                if found:
                                    break


# Driver code
pygame.init()
size = 1000, 800
screen = pygame.display.set_mode(size)
game_logic = Logic()
View(size, game_logic)
