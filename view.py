import pygame
import sys

class View:

    """Renders view for frontend client

    Responsible for rendering the frontend view. After initialization,
    calls to render_grid(), render_hand(), and render_details() can be
    performed automatically by calling update_view()
    """

    def __init__(self):
        """Inits the view."""
        pygame.init()
        window_size = 1000, 800
        background_color = (255, 255, 255)
        screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Qwirkle")
        screen.fill(background_color)
        pygame.display.flip()

    def update_view():
        """Updates the entire view."""
        pass

    def render_grid():
        """Renders the main grid on which tiles may be placed."""
        pass

    def render_hand():
        """Renders the tiles currently held by the player."""
        pass

    def render_details():
        """Renders details such as the server IP and the player's score."""
        pass

    def init_event_loop(self):
        """Event loop for handling UI interaction """
        running = True
        while(running):
            for ev in  pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()


# Test code - ignore
game_view = View()
game_view.init_event_loop()
