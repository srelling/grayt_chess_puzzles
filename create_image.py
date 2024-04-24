import chess
import pandas as pd
import chess.svg
import cairosvg
from PIL import Image
import datetime
import os

def make_gray(image_path, output_path):
    # Open an image file
    with Image.open(image_path) as img:
        # Convert image to RGB (in case it's a different format)
        img = img.convert('RGB')
        
        # Load the pixel data
        pixels = img.load()
        
        # Get image dimensions
        width, height = img.size
        
        # Define the target colors
        green = (124, 148, 93)
        beige = (238, 237, 213)
        black = (0, 0, 0)
        white = (255, 255, 255)
        whtie2 = (236, 236, 236)
        gray = (98, 98, 98)
        
        # Iterate over all pixels
        for x in range(width):
            for y in range(height):
                #if r g b are all the same make it gray
                r, g, b = pixels[x, y]
                if pixels[x, y] != green and pixels[x, y] != beige:
                    # Check if pixel is close to the border
                    boarder_thickness = 95
                    if x < boarder_thickness or x > width - boarder_thickness or y < boarder_thickness or y > height - boarder_thickness:
                        continue
                    # Change black or white pixels to gray
                    pixels[x, y] = gray
        
        # Save the modified image
        img.save(output_path)

def make_gray_png(fen, puzzle_id, what_mate, white_pieces, black_pieces):
    board = chess.Board(fen)
    boardsvg = chess.svg.board(flipped=False, coordinates=True, board = board, size=350, colors={"square light": "#eeedd5", "square dark": "#7c945d", "square dark lastmove": "#7c945d", "square light lastmove": "#eeedd5"})
    f = open("position.svg", "w")
    f.write(boardsvg)
    f.close()
    img = cairosvg.svg2png(url='position.svg', write_to=f'grayt_puzzles/puzzle_{puzzle_id}_M{what_mate}_W{white_pieces}_B{black_pieces}.png', scale=7)
    make_gray(f'grayt_puzzles/puzzle_{puzzle_id}_M{what_mate}_W{white_pieces}_B{black_pieces}.png', f'grayt_puzzles/puzzle_{puzzle_id}_M{what_mate}_W{white_pieces}_B{black_pieces}_gray.png')
    # delete the original png and svg files
    os.remove('position.svg')
    

# read the csv file and turn all fen strings into images using the make_png function
df = pd.read_csv('grayt_puzzles.csv')

# create one gray and one colored image for each puzzle
for index, row in df.iterrows():
    make_gray_png(row['FEN'], row['PuzzleId'], row['what_mate'], row['white_pieces'], row['black_pieces'])

