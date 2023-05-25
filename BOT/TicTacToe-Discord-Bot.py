import discord
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Setting the bot prefix
prefix = "#"
token = "YOUR_DISCORD_TOKEN"
board = []
players = []
current_player = None

# Function to create a new board
def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

# Function to print the current board
def print_board(board):
    line = '-------------'
    output = line + '\n'
    for row in board:
        output += '|'
        for cell in row:
            output += f' {cell} |'
        output += '\n' + line + '\n'
    return output

# Function to check if a player has won
def check_win(board, player):
    for i in range(3):
        if board[i] == [player, player, player]:
            return True
        if [board[0][i], board[1][i], board[2][i]] == [player, player, player]:
            return True
    if [board[0][0], board[1][1], board[2][2]] == [player, player, player]:
        return True
    if [board[2][0], board[1][1], board[0][2]] == [player, player, player]:
        return True
    return False

# Function to get the current player number
def get_current_player_number():
    if current_player == players[0]:
        return 1
    elif current_player == players[1]:
        return 2
    else:
        return None

# Function to process bot commands
async def process_commands(message):
    global board
    global players
    global current_player

    if message.content.startswith(prefix):
        command = message.content[len(prefix):].strip().lower()

        if command == 'start':
            if message.author.id not in [p.id for p in players]:
                if len(players) < 2:
                    players.append(message.author)
                    await message.channel.send(f'Tic-Tac-Toe game started! {message.author.mention} is player {len(players)}.')
                    
                    if len(players) == 2:
                        board = create_board()
                        output = print_board(board)
                        current_player = players[0]
                        await message.channel.send('The board has been initialized. Player 1, it\'s your turn!')
                        await message.channel.send(f'```\n{output}\n```')
                    else:
                        await message.channel.send('Waiting for the second player...')

                else:
                    await message.channel.send(f'{message.author.mention}, the game is already in progress with 2 players!')

            else:
                await message.channel.send(f'{message.author.mention}, you are already participating in the game!')

        elif command == 'stop':
            if message.author.id in [p.id for p in players]:
                players = [p for p in players if p.id != message.author.id]
                await message.channel.send(f'{message.author.mention}, you have left the game.')
            else:
                await message.channel.send(f'{message.author.mention}, you are not participating in the game.')

        elif command.startswith('play'):
            if message.author.id in [p.id for p in players]:
                if len(players) == 2:
                    if current_player != message.author:
                        await message.channel.send(f'{message.author.mention}, it\'s not your turn.')
                        return

                    player_index = [p.id for p in players].index(message.author.id)
                    player_number = player_index + 1
                    other_player_number = 2 if player_number == 1 else 1
                    player = 'X' if player_number == 1 else 'O'
                    other_player = 'O' if player_number == 1 else 'X'

                    move = command[len('play'):].strip().lower()
                    if not move.isdigit() or int(move) < 1 or int(move) > 9:
                        await message.channel.send(f'{message.author.mention}, invalid move. Use a number from 1 to 9.')
                    else:
                        move = int(move) - 1
                        row = move // 3
                        col = move % 3
                        if board[row][col] != ' ':
                            await message.channel.send(f'{message.author.mention}, position already occupied. Choose another position.')
                        else:
                            board[row][col] = player
                            output = print_board(board)
                            await message.channel.send(f'```\n{output}\n```')
                            if check_win(board, player):
                                await message.channel.send(f'Congratulations, {message.author.mention}! You won!')
                                players = []
                                board = []
                                current_player = None
                            elif ' ' not in [cell for row in board for cell in row]:
                                await message.channel.send('It\'s a tie!')
                                players = []
                                board = []
                                current_player = None
                            else:
                                current_player = players[other_player_number - 1]
                                await message.channel.send(f'Player {other_player_number}, it\'s your turn!')

                else:
                    await message.channel.send('Waiting for the second player...')

            else:
                await message.channel.send(f'{message.author.mention}, you are not participating in the game.')

        elif command == 'help':
            help_message = """
TIC-TAC-TOE COMMANDS

#start: Start the Tic-Tac-Toe game.

#stop: Quit the Tic-Tac-Toe game.

#play <position>: Make a move in the Tic-Tac-Toe game. Replace <position> with a number from 1 to 9 to choose a position on the board.

#help: Display this help message.
"""
            await message.channel.send(f'```\n{help_message}\n```')

# Bot initialization event
@client.event
async def on_ready():
    print(f'Bot connected as {client.user.name}')
    print('------')

# Message received event
@client.event
async def on_message(message):
    await process_commands(message)

# Run the bot
client.run(token)
