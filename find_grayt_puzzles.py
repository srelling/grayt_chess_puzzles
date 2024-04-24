from stockfish import Stockfish
import chess
import pandas as pd
import numpy as np

# Path to the Stockfish executable
stockfish_path = '/root/censored_chess_puzzle/stockfish/stockfish-ubuntu-x86-64-avx2'  # Update this path
stockfish = Stockfish(stockfish_path)


def change_piece_color(fen, index):
    pieces = 'rnbqpRNBQP'
    count = 0
    new_fen = ''
    for char in fen.split()[0]:
        if char in pieces:
            if count == index:
                char = char.swapcase()
            count += 1
        new_fen += char
        
    for part in fen.split()[1:]:
        new_fen += ' ' + part
    return new_fen


def swap_kings(fen):
    parts = fen.split()
    parts[0] = parts[0].replace('k', 's').replace('K', 'k').replace('s', 'K')
    return ' '.join(parts)


def change_turn(fen):
    parts = fen.split()
    parts[1] = 'w' if parts[1] == 'b' else 'b'
    return ' '.join(parts)


def update_fen(fen, moves):
    board = chess.Board(fen)
    first_move = moves.split()[0]
    move = chess.Move.from_uci(first_move)
    if move in board.legal_moves:
        board.push(move)
        return board.fen()
    else:
        return fen


def count_pieces(fen):
    pieces = np.array(list('rnbqkpRNBQKP'))
    chars = np.array(list(fen.split()[0]))
    return np.sum(np.isin(chars, pieces))


def count_pawns(fen):
    pieces = np.array(list('pP'))
    chars = np.array(list(fen.split()[0]))
    return np.sum(np.isin(chars, pieces))


def count_non_pawn_pieces(fen):
    pieces = np.array(list('rnbqkRNBQK'))
    chars = np.array(list(fen.split()[0]))
    return np.sum(np.isin(chars, pieces))


def count_white_pieces(fen):
    pieces = np.array(list('RNBQKP'))
    chars = np.array(list(fen.split()[0]))
    return np.sum(np.isin(chars, pieces))


def count_black_pieces(fen):
    pieces = np.array(list('rnbqkp'))
    chars = np.array(list(fen.split()[0]))
    return np.sum(np.isin(chars, pieces))


def is_fen_matein1(fen):
    board = chess.Board(fen)
    if not board.is_valid():
        return False
    if board.is_game_over():
        return False
    stockfish.set_fen_position(fen)
    evaluation = stockfish.get_evaluation()
    type = evaluation['type']
    value = evaluation['value']
    if type == 'mate' and (value == 1 or value == -1):
        return True


def is_fen_lower_mate(fen, white_pieces, black_pieces, what_mate):
    new_white_pieces = count_white_pieces(fen)
    new_black_pieces = count_black_pieces(fen)
    if new_white_pieces != white_pieces or new_black_pieces != black_pieces:
        return False
    board = chess.Board(fen)
    if not board.is_valid():
        return False
    if board.is_game_over():
        return False
    try:
        stockfish.set_fen_position(fen)
        evaluation = stockfish.get_evaluation()
    except Exception:
        return True
    type = evaluation['type']
    value = evaluation['value']
    if type == 'mate':
        return value <= what_mate
    else:
        return False


def what_mate(fen):
    stockfish.set_fen_position(fen)
    evaluation = stockfish.get_evaluation()
    type = evaluation['type']
    value = evaluation['value']
    if type == 'mate':
        return value
    else:
        return 0


def check_colorless_matein1_rec(fen, index, is_changed):
    if index >= (count_pieces(fen) - 2):
        if is_changed:
            return is_fen_matein1(fen)
        else:
            return False
    
    if check_colorless_matein1_rec(fen, index + 1, is_changed):
        return True
    
    if check_colorless_matein1_rec(change_piece_color(fen, index), index + 1, True):
        return True
    
    return False


def check_colorless_matein1(fen):
    if check_colorless_matein1_rec(fen, 0, False):
        return False
    
    if check_colorless_matein1_rec(swap_kings(fen), 0, False):
        return False
    
    return True


def check_colorless_mate_rec(fen, index, is_changed, piece_count, white_pieces, black_pieces, what_mate):
    if index >= (piece_count - 2):
        if is_changed:
            return is_fen_lower_mate(fen, white_pieces, black_pieces, what_mate)
        else:
            return False
    
    if check_colorless_mate_rec(fen, index + 1, is_changed, piece_count, white_pieces, black_pieces, what_mate):
        return True
    
    if check_colorless_mate_rec(change_piece_color(fen, index), index + 1, True, piece_count, white_pieces, black_pieces, what_mate):
        return True
    
    return False


def check_colorless_mate(fen, piece_count, white_pieces, black_pieces, what_mate):
    if check_colorless_mate_rec(fen, 0, False, piece_count, white_pieces, black_pieces, what_mate):
        return False
    
    if check_colorless_mate_rec(swap_kings(fen), 0, False, piece_count, white_pieces, black_pieces, what_mate):
        return False
    
    return True


df = pd.read_csv('mate_puzzles_m.csv')

print("Initial Data:")
print(df.info())
print(df.head(10))

df = df[df['FEN'].str.contains(' b ') == False]

df.loc[:, 'piece_count'] = df['FEN'].apply(count_non_pawn_pieces)
df_f1 = df[(df['piece_count'] >= 5) & (df['piece_count'] <= 8)]

print("After sorting by piece count:")
print(df_f1.info())
print(df_f1.head(10))

df_f1.loc[:, 'pawn_count'] = df_f1['FEN'].apply(count_pawns)
df_f2 = df_f1[df_f1['pawn_count'] <= 3]

print("After sorting by pawn count:")
print(df_f2.info())
print(df_f2.head(10))

df_f2.loc[:, 'what_mate'] = df_f2['FEN'].apply(what_mate)
df_f2.loc[:, 'piece_count'] = df_f2['FEN'].apply(count_pieces)
df_f2.loc[:, 'white_pieces'] = df_f2['FEN'].apply(count_white_pieces)
df_f2.loc[:, 'black_pieces'] = df_f2['FEN'].apply(count_black_pieces)

print("After adding new cols:")
print(df_f2.info())
print(df_f2.head(10))

df_f3 = df_f2[df_f2.apply(lambda row: check_colorless_mate(row['FEN'], row['piece_count'], row['white_pieces'], row['black_pieces'], row['what_mate']), axis=1)]

sorted_df = df_f3.sort_values(by=['Rating'], ascending=[False])
sorted_df.to_csv('grayt_puzzles.csv', index=False)

print("CSV with cool Puzzles found!")
