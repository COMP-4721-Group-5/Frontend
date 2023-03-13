from lib.shared.network_exchange_format import ServerResponse

flag = -1

valid = True
first = True
start_turn = True
game_over = False
winner = False

flag = ((ServerResponse.ResponseFlag.VALID if valid else 0) |
        (ServerResponse.ResponseFlag.FIRST if first else 0) |
        (ServerResponse.ResponseFlag.START_TURN if start_turn else 0) |
        (ServerResponse.ResponseFlag.GAME_OVER if game_over else 0) |
        (ServerResponse.ResponseFlag.WINNER if winner else 0)
       ) if flag < 0 else ServerResponse.ResponseFlag(flag)

print(flag)
