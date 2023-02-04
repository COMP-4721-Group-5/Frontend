import pygame
import sys

class View:

    """Renders view for frontend client

    Responsible for rendering the frontend view. After initialization,
    calls to render_grid(), render_hand(), and render_details() can be
    performed automatically by calling update_view(). The event loop is
    for handling basic view-related events, such as closing the window
    or dragging and dropping a tile onto the grid.
    """

    TOP_LEFT_X = 108
    TOP_LEFT_Y = 108
    FRAME_SIZE = 8
    SELECTED_TILE = "NONE"
    WINDOW_SIZE = 0,0
    SCREEN = "NONE"
    hand = ["EMPTY", pygame.image.load('favicon.png'), "EMPTY", "EMPTY", "EMPTY", "EMPTY"] # temporary for testing

    def __init__(self, size):
        """Inits the view"""
        self.WINDOW_SIZE = size
        self.SCREEN = pygame.display.set_mode(size)
        favicon = pygame.image.load('favicon.png')
        pygame.display.set_icon(favicon)
        background_color = (255, 255, 255)
        pygame.display.set_caption("Qwirkle")
        self.SCREEN.fill(background_color)
        self.update_view()
        self.init_event_loop()

    def update_view(self):
        """Updates the entire view.

            Args:
                screen: screen object returned by pygame.display.set_mode()
                window_size: dimensions of the Qwirkle window
                top_left_x: x coordinate for top-left tile of frame
                top_left_y: y coordinate for top-left tile of frame

            Returns:
                Nothing
        """
        self.render_grid(self.SCREEN, self.WINDOW_SIZE, self.TOP_LEFT_X, self.TOP_LEFT_Y)
        self.render_hand(self.SCREEN, self.WINDOW_SIZE)
        self.render_details()
        pygame.display.flip()

    def render_grid(self, screen, window_size, top_left_x, top_left_y):
        """Renders the main grid on which tiles may be placed.

            Args:
                screen: screen object returned by pygame.display.set_mode()
                window_size: dimensions of the Qwirkle window

            Returns:
                Nothing
        """
        border_color = (0, 0, 0)
        background_color = (255, 255, 255)
        self.draw_hollow_rect(screen, background_color, border_color, (0.09 * window_size[0]), (0.05 * window_size[1]), (0.8 * window_size[0]), (0.8 * window_size[1]), 10)

        num_rows = self.FRAME_SIZE
        num_cols = self.FRAME_SIZE
        tile_width = 1 + ((0.8 * window_size[0]) - (5 * 2)) / num_rows
        tile_height = 1 + ((0.8 * window_size[1]) - (5 * 2)) / num_cols

        x_pos = (0.09 * window_size[0]) + 10
        y_pos = (0.05 * window_size[1]) + 10

        for i in range(num_rows):
            x_pos = (0.09 * window_size[0]) + 10
            for j in range(num_cols):
                self.draw_hollow_rect(screen, background_color, border_color, x_pos, y_pos, tile_width, tile_height, 5)
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
        self.draw_hollow_rect(screen, background_color, border_color, x_pos - 10, y_pos - 5, 5 + tile_width * 6, tile_height + 10, 15)
        for i in range(num_tiles + 1):
            if self.SELECTED_TILE == i:
                border_color = (255, 0, 255)
            if i < 6:
                self.draw_hollow_rect(screen, background_color, border_color, x_pos, y_pos, tile_width, tile_height, 5)
                if self.hand[i] != "EMPTY":
                    curr_tile = self.hand[i]
                    tile_img = pygame.transform.scale(curr_tile, (tile_width - 10, tile_height - 10))
                    screen.blit(tile_img, (x_pos + 5, y_pos + 5))
            if i == 7:
                self.draw_hollow_rect(screen, background_color, border_color, x_pos, y_pos, tile_width, tile_height, 5)
            x_pos = x_pos + tile_width - 2
            border_color = (0, 0, 0)

    def render_details(self):
        """Renders details such as the server IP and the player's score."""
        pass

    def draw_hollow_rect(self, screen, color, border_color, x, y, width, height, border_width):
        """Draws a hollow rectangle

            Args:
                screen: screen object returned by pygame.display.set_mode()
                color: the background color
                border_color: the color of the border
                x: x position of the top left corner
                y: y position of the top left corner
                width: width of the recelf.
                height: height of the rect
                border_width: width of the border

            Returns:
                Nothing
        """
        pygame.draw.rect(screen, border_color, pygame.Rect(x, y, width, height))
        pygame.draw.rect(screen, color, pygame.Rect(x + border_width, y + border_width, width - (2 * border_width), height - (2 * border_width)))

    def init_event_loop(self):
        """Event loop for handling UI interaction """
        running = True
        while(running):
            for ev in  pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]                  
                    tile_width = 90
                    gap_width = 8
                    total_width = 585
                    if (100 < x < 685) and (700 < y < 770):
                        relative_x = x - 100                 
                        for i in range(6):
                            if relative_x < (tile_width + (gap_width / 2)) * (i + 1):
                                self.SELECTED_TILE = i
                                self.update_view()
                                break

# Test code
pygame.init()
size = 1000, 800
screen = pygame.display.set_mode(size)
View(size)
