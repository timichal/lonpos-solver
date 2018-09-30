from piece_defs import pieces

# pieces: a dict of possible pieces

with open("input") as file:
    input_field = [line.strip() for line in file]

#pieces: A-L, every one can be used only once
def find_missing_pieces(input_field):
    missing_pieces = [piece for piece in pieces]
    for line in input_field:
        for pos in line:
            if pos in missing_pieces:
                missing_pieces.remove(pos)
    return missing_pieces

def piece_turner(piece):
    piece_variants = []
    
    # normal-basic
    piece_variants.append(piece)
    # reverse-basic
    piece_reverse = [line[::-1] for line in piece]
    piece_variants.append(piece_reverse)
    # normal-180
    piece_variants.append(piece_reverse[::-1])
    # reverse-180
    piece_variants.append(piece[::-1])
    # reverse-R
    piece_reverse_r = [["." for x in range(len(piece))] for y in range(len(piece[0]))]
    for x, line in enumerate(piece):
        for y, char in enumerate(line):
            if char != ".":
                piece_reverse_r[y][x] = char
    piece_reverse_r = [''.join(line) for line in piece_reverse_r]
    piece_variants.append(piece_reverse_r)
    # normal-R
    piece_variants.append(piece_reverse_r[::-1])
    # normal-L
    piece_normal_l = [line[::-1] for line in piece_reverse_r]
    piece_variants.append(piece_normal_l)
    # reverse-L
    piece_variants.append(piece_normal_l[::-1])

    turned_pieces = []
    for variant in piece_variants:
        if variant not in turned_pieces:
            turned_pieces.append(variant)
    return turned_pieces

def missing_piece_coords(input_field):
    missing_pieces = find_missing_pieces(input_field)
    missing_piece_coords = {}
    for piece in missing_pieces:
        variants_coords = []
        for current_piece in piece_turner(pieces[piece]):
            current_piece_coords = []
            for xpos, line in enumerate(current_piece):
                for ypos, char in enumerate(line):
                    if char != ".":
                        current_piece_coords.append((xpos, ypos))
            variants_coords.append(current_piece_coords)
        missing_piece_coords[piece] = variants_coords
    return missing_piece_coords

def find_first_empty(field):
    for x, line in enumerate(field):
        for y, char in enumerate(line):
            if char == ".":
                return (x, y)

def unfilled(field):
    for line in field:
        if "." in line:
            return True
    return False

def fill_with_piece(piece, variant, input_field, empty_pos):
    field = [list(line) for line in input_field]
    # if starting at (0,1), need to reset it to (0,0)
    yoffset = 0-variant[0][1]
    
    try: 
        for position in variant:
            pos_x = empty_pos[0]+position[0]
            pos_y = empty_pos[1]+position[1]+yoffset
            if field[pos_x][pos_y] == ".":
                field[pos_x][pos_y] = piece
                #for line in field: print(line)
            else:
                return False
        return [''.join(line) for line in field]
    except:
        #print("didnt fit!")
        return False

def newfill(field):
    pool = missing_piece_coords(field)
    empty_pos = find_first_empty(field)
    for item in pool:
        for variant in pool[item]:
            #print(field, item, variant)
            if fill_with_piece(item, variant, field, empty_pos):
                #print("fillable!")
                newfield = fill_with_piece(item, variant, field, empty_pos)
                newfield = newfill(newfield)
                if not unfilled(newfield):
                    field = newfield
    return field

res = newfill(input_field)
if type(res) is list:
    for line in res:
        print(''.join(line))