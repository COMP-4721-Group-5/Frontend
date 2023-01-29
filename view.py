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

    def __init__(self):
        """Inits the view."""
        pygame.init()
        window_size = 1000, 800
        background_color = (255, 255, 255)
        screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Qwirkle")
        screen.fill(background_color)
        self.update_view(screen, window_size)
        self.init_event_loop()

    def update_view(self, screen, window_size):
        """Updates the entire view."""
        self.render_grid(screen, window_size)
        self.render_hand()
        self.render_details()
        pygame.display.flip()

    def render_grid(self, screen, window_size):
        """Renders the main grid on which tiles may be placed."""
        border_color = (0, 0, 0)
        background_color = (255, 255, 255)
        self.draw_hollow_rect(screen, background_color, border_color, (0.05 * window_size[0]), (0.05 * window_size[1]), (0.9 * window_size[0]), (0.8 * window_size[1]), 10)

    def render_hand(self):
        """Renders the tiles currently held by the player."""
        pass

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
        pygame.draw.rect(screen, color, pygame.Rect(x+border_width, y+border_width, width - (2 * border_width), height - (2 * border_width)))

    def init_event_loop(self):
        """Event loop for handling UI interaction """
        running = True
        while(running):
            for ev in  pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()

# Test code
View()
