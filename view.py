from typing import List
import sys
import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
from PIL import ImageTk, Image
import numpy as np
import numpy.typing as npt
import pygame

from lib.shared.player import Player
from lib.frontend.logic import Logic
from lib.frontend.frontend_network import ClientSocket
from lib.frontend.frontend_network import DataReceivedEvent, GameEndEvent
from lib.shared.internal_structures import Board, Placement, Tile
from lib.shared.network_exchange_format import ServerResponse


def tile_img_load(tile: Tile):
    """Method for getting the images for the tile

    Args:
        tile: Tile to load to an image

    Returns:
        The image of the tile.
    """
    if tile == 0:
        return None
    fileName = "assets/tile_img/%s-%s.png" % (
        tile.color.name.lower(),
        tile.shape.name.lower(),
    )
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
        __selected_board_tile: Tracks tiles selected on the board
        __selected_board_x_y: Tracks x,y coordinate of selected tile on the board
    """

    __top_left_x: int = 108
    __top_left_y: int = 108
    __frame_size: int = 8
    __selected_tile: int = -1
    __window_size = 0, 0
    __screen = None
    __logic: Logic = None
    __board: Board = None
    __socket: ClientSocket
    __discarding_tiles: List[int]
    __selected_board_tile: Tile
    __selected_board_x_y: npt.NDArray[np.int_]
    __is_winner: bool

    def __init__(self, size, g_logic):
        """Inits the view"""
        self.__logic = g_logic
        self.__window_size = size
        self.__socket = View.connect_server()
        self.__screen = pygame.display.set_mode(size)
        self.__board = self.__logic.board
        self.__discarding_tiles = list()
        self.__is_winner = False
        self.__selected_board_tile = None
        self.__selected_board_x_y = np.full(2, -1, np.int_)
        favicon = pygame.image.load("assets/favicon.png")
        pygame.display.set_icon(favicon)
        background_color = (255, 255, 255)
        pygame.display.set_caption("Qwirkle")
        self.__screen.fill(background_color)
        self.update_view()
        self.render_details()
        self.render_instructions()  # Fix window geometry before uncommenting
        try:
            self.init_event_loop()
        except Exception as ex:
            self.__socket.close()
            raise ex
        except KeyboardInterrupt as ki:
            self.__socket.close()
            raise ki

    def render_instructions(self):
        """Renders the instructions when the game is launched

        Returns:
            Nothing
        """
        ins_window_size = (500, 500)
        root = tk.Tk()
        root.withdraw()
        gamerules_png = Image.open("assets/instructions/GameRule.png")
        gamerules_png = gamerules_png.resize(ins_window_size)
        gamerules_png = ImageTk.PhotoImage(gamerules_png)
        instructions_png = Image.open("assets/instructions/PlayInstruct.png")
        instructions_png = instructions_png.resize(ins_window_size)
        instructions_png = ImageTk.PhotoImage(instructions_png)
        scoreguide_png = Image.open("assets/instructions/ScoreGuide.png")
        scoreguide_png = scoreguide_png.resize(ins_window_size)
        scoreguide_png = ImageTk.PhotoImage(scoreguide_png)
        win1 = tk.Toplevel(root)
        win1.title("Game Rules")
        gr_label = tk.Label(win1, image=gamerules_png)
        gr_label.pack()
        win1.wait_window()
        win2 = tk.Toplevel(root)
        win2.title("Instructions")
        ins_label = tk.Label(win2, image=instructions_png)
        ins_label.pack()
        win2.wait_window()
        win3 = tk.Toplevel(root)
        win3.title("Score Guide")
        sc_label = tk.Label(win3, image=scoreguide_png)
        sc_label.pack()
        win3.wait_window()
        root.destroy()

    def update_view(self):
        """Updates the entire view.

        Returns:
            Nothing
        """
        self.render_grid(
            self.__screen, self.__window_size, self.__top_left_x, self.__top_left_y
        )
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
        self.draw_hollow_rect(
            screen,
            background_color,
            border_color,
            (0.09 * window_size[0]),
            (0.05 * window_size[1]),
            (0.8 * window_size[0]),
            (0.8 * window_size[1]),
            10,
        )
        num_rows = self.__frame_size
        num_cols = self.__frame_size
        tile_width = 1 + ((0.8 * window_size[0]) - (5 * 2)) / num_rows
        tile_height = 1 + ((0.8 * window_size[1]) - (5 * 2)) / num_cols
        x_pos = (0.09 * window_size[0]) + 10
        y_pos = (0.05 * window_size[1]) + 10
        for i in range(num_rows):
            x_pos = (0.09 * window_size[0]) + 10
            for j in range(num_cols):
                self.draw_hollow_rect(
                    screen,
                    background_color,
                    border_color,
                    x_pos,
                    y_pos,
                    tile_width,
                    tile_height,
                    5,
                )
                curr_tile = self.__board.get_tile(
                    self.__top_left_x + j, self.__top_left_y + i
                )
                if curr_tile != 0:
                    if curr_tile == self.__selected_board_tile:
                        border_color = (255, 0, 255)
                        self.draw_hollow_rect(
                            screen,
                            background_color,
                            border_color,
                            x_pos,
                            y_pos,
                            tile_width,
                            tile_height,
                            5,
                        )
                        border_color = (0, 0, 0)
                    tile_img = pygame.transform.scale(
                        tile_img_load(curr_tile), (tile_width - 10, tile_height - 10)
                    )
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
        x_pos = (0.09 * window_size[0]) + 10
        y_pos = ((0.05 * window_size[1]) + 8) + (8 * tile_height) + gap
        self.draw_hollow_rect(
            screen,
            background_color,
            border_color,
            x_pos - 10,
            y_pos - 5,
            5 + tile_width * 6,
            tile_height + 10,
            15,
        )
        for i in range(num_tiles + 1):
            if self.__selected_tile == i:
                border_color = (255, 0, 255)
            if i in self.__discarding_tiles:
                border_color = (255, 0, 0)
            if i < 6:
                self.draw_hollow_rect(
                    screen,
                    background_color,
                    border_color,
                    x_pos,
                    y_pos,
                    tile_width,
                    tile_height,
                    5,
                )
                if self.__logic.player[i] is not None:
                    curr_tile = self.__logic.player[i]
                    tile_img = pygame.transform.scale(
                        tile_img_load(curr_tile), (tile_width - 10, tile_height - 10)
                    )
                    screen.blit(tile_img, (x_pos + 5, y_pos + 5))
            if i == 7:
                self.draw_hollow_rect(
                    screen,
                    background_color,
                    border_color,
                    x_pos,
                    y_pos,
                    tile_width,
                    tile_height,
                    5,
                )
            x_pos = x_pos + tile_width - 2
            border_color = (0, 0, 0)
        if self.__logic.is_curr_turn and (
            self.__logic.tile_played() or len(self.__discarding_tiles) != 0
        ):
            confirm_image = pygame.transform.scale(
                pygame.image.load("assets/buttons/confirm-image.png"),
                (tile_width - 9, tile_height - 9),
            )
            screen.blit(confirm_image, (789, 770 - tile_height + 10))

    def render_details(self):
        """Renders details such as the server IP and the player's score."""
        connected_color = (50, 205, 50)
        black_color = (0, 0, 0)
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 15)
        server_ip = self.__socket.address
        server_port = self.__socket.port
        con_surface = font.render("Connected: ", True, connected_color)
        ip_str = str(server_ip) + ":" + str(server_port)
        ip_surface = font.render(ip_str, True, black_color)

        score = self.__logic.player.score
        score_surface = font.render("Score: " + str(score), True, black_color)
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, 995, 35))

        screen.blit(score_surface, (90, 17))
        screen.blit(con_surface, (715, 14))
        screen.blit(ip_surface, (795, 14))
        pygame.display.flip()

    def draw_hollow_rect(
        self, screen, color, border_color, x, y, width, height, border_width
    ):
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
            screen,
            color,
            pygame.Rect(
                x + border_width,
                y + border_width,
                width - (2 * border_width),
                height - (2 * border_width),
            ),
        )

    def connect_server():
        """Prompts user for server address and port."""
        server_ip = tkinter.simpledialog.askstring("Connect", "Server IP:")
        server_port = tkinter.simpledialog.askinteger(
            "Connect", "Server Port:", minvalue=1
        )

        return ClientSocket(server_ip, server_port)

    def init_event_loop(self):
        """Event loop for handling UI interaction"""

        running = True
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    if tkinter.messagebox.askokcancel(
                        title="Quit Qwirkle?", message="Confirm quit?"
                    ):
                        self.__socket.close()
                        sys.exit()
                if ev.type == DataReceivedEvent.EVENTTYPE:
                    # TODO: Use data from event to update internal data
                    self.__logic.is_curr_turn = (
                        ServerResponse.ResponseFlag.START_TURN in ev.dict["flag"]
                    )
                    self.__logic.is_first_turn = (
                        ServerResponse.ResponseFlag.FIRST in ev.dict["flag"]
                    )
                    self.__board = ev.dict["curr_board"]
                    for i in range(len(ev.dict["curr_hand"])):
                        self.__logic.player[i] = ev.dict["curr_hand"][i]
                    self.__logic.player.score = ev.dict["scores"][ev.dict["user_id"]]
                    running = (
                        ServerResponse.ResponseFlag.GAME_OVER not in ev.dict["flag"]
                    )
                    self.__is_winner = (
                        ServerResponse.ResponseFlag.WINNER in ev.dict["flag"]
                    )
                    self.update_view()
                if ev.type == GameEndEvent.EVENTTYPE:
                    if running:
                        tkinter.messagebox.showerror(
                            "Connection Lost", "Connection lost with server. Exiting."
                        )
                    elif self.__is_winner:
                        tkinter.messagebox.showinfo(
                            "Winner!",
                            f"You won with {self.__logic.player.score} points!",
                        )
                    else:
                        tkinter.messagebox.showinfo(
                            "Good game",
                            f"You lost with {self.__logic.player.score} points.",
                        )
                    sys.exit()
                if ev.type == pygame.KEYDOWN:  # Handle navigation
                    if not self.__logic.is_first_turn:
                        if ev.key == pygame.K_UP:
                            self.__top_left_y = self.__top_left_y - 1
                        if ev.key == pygame.K_DOWN:
                            self.__top_left_y = self.__top_left_y + 1
                        if ev.key == pygame.K_LEFT:
                            self.__top_left_x = self.__top_left_x - 1
                        if ev.key == pygame.K_RIGHT:
                            self.__top_left_x = self.__top_left_x + 1
                        self.update_view()
                if ev.type == pygame.MOUSEBUTTONDOWN and self.__logic.is_curr_turn:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]

                    tile_width = 90
                    gap_width = 8
                    total_width = 585

                    if (
                        (789 < x < 878)
                        and (699 < y < 770)
                        and self.__logic.is_curr_turn
                        and (
                            self.__logic.tile_played()
                            or len(self.__discarding_tiles) != 0
                        )
                    ):  # Confirm move
                        if self.__logic.tile_played() == False:  # Remove tiles
                            self.__discarding_tiles.clear()
                            self.__logic.end_turn(True, self.__socket)
                        else:  # Play tiles
                            self.__logic.end_turn(False, self.__socket)
                    if (100 < x < 685) and (
                        700 < y < 770
                    ):  # Handles interaction with hand
                        if (
                            ev.button == 1 and len(self.__discarding_tiles) == 0
                        ):  # Select a tile for placing
                            relative_x = x - 100
                            for i in range(6):
                                if relative_x < (585 / 6) * (i + 1):
                                    self.__selected_tile = i

                                    if (
                                        self.__selected_board_tile != 0
                                        and self.__logic.player[i] == None
                                        and self.__selected_board_x_y[0] != -1
                                    ):
                                        self.__logic.player[
                                            i
                                        ] = self.__selected_board_tile
                                        self.__logic.undo_play(
                                            Placement(
                                                self.__selected_board_tile,
                                                self.__selected_board_x_y[0],
                                                self.__selected_board_x_y[1],
                                            )
                                        )
                                        self.__selected_board_tile = None
                                        self.__board.remove_tile(
                                            self.__selected_board_x_y[0],
                                            self.__selected_board_x_y[1],
                                        )
                                        self.__selected_board_x_y.fill(-1)

                                    self.update_view()
                                    break
                        elif ev.button == 3 and not self.__logic.tile_played():
                            # Select a tile for discarding
                            relative_x = x - 100
                            for i in range(6):
                                if relative_x < (585 / 6) * (i + 1):
                                    if i in self.__discarding_tiles:
                                        self.__discarding_tiles.remove(i)
                                        self.__logic.undo_discard(i)
                                    else:
                                        self.__selected_tile = -1
                                        self.__discarding_tiles.append(i)
                                        self.__logic.discard_tile(
                                            self.__logic.player[i], i
                                        )
                                    self.update_view()
                                    break
                    elif (100 < x < 877) and (53 < y < 667):
                        relative_x = x - 100
                        relative_y = y - 53
                        found = False
                        for i in range(self.__frame_size):
                            if relative_x < (777 / self.__frame_size) * (i + 1):
                                for j in range(self.__frame_size):
                                    if relative_y < (615 / self.__frame_size) * (j + 1):
                                        placement = Placement(  # Creates and registers placement
                                            self.__logic.player[self.__selected_tile],
                                            self.__top_left_x + i,
                                            self.__top_left_y + j,
                                        )
                                        self.__selected_board_x_y[0] = (
                                            self.__top_left_x + i
                                        )
                                        self.__selected_board_x_y[1] = (
                                            self.__top_left_y + j
                                        )
                                        if (
                                            self.__board.get_tile(
                                                self.__selected_board_x_y[0],
                                                self.__selected_board_x_y[1],
                                            )
                                            != 0
                                        ) and self.__board.get_tile(
                                            self.__selected_board_x_y[0],
                                            self.__selected_board_x_y[1],
                                        ).is_temporary():
                                            self.__selected_board_tile = self.__board.get_tile(
                                                self.__top_left_x
                                                + i,  # Need to verify tile is temporary
                                                self.__top_left_y + j,
                                            )
                                        if (
                                            (
                                                self.__logic.player[
                                                    self.__selected_tile
                                                ]
                                                is not None
                                            )
                                            and (self.__selected_tile >= 0)
                                            and (
                                                self.__board.get_tile(
                                                    self.__selected_board_x_y[0],
                                                    self.__selected_board_x_y[1],
                                                )
                                                == 0
                                            )
                                        ):
                                            self.__board.add_tile(placement)
                                            self.__logic.play_tile(placement)
                                            self.__logic.player[
                                                self.__selected_tile
                                            ] = None
                                            self.__selected_tile = -1
                                            self.update_view()
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
