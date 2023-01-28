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
        pygame.draw.rect(screen, border_color, pygame.Rect((0.05 * window_size[0]), (0.05 * window_size[1]), (0.9 * window_size[0]), (0.8 * window_size[1])))
		# TODO: implement hollow_rect(), replace previous line & use for grid generation

    def render_hand(self):
        """Renders the tiles currently held by the player."""
        pass

    def render_details(self):
        """Renders details such as the server IP and the player's score."""
        pass

    def hollow_rect(self, x, y, width, height, border_width):
        """Returns a hollow rectangle"""
        pass

    def init_event_loop(self):
        """Event loop for handling UI interaction """
        running = True
        while(running):
            for ev in  pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()

# Test code
View()
