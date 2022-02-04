import tkinter as tk
import random
import linecache


def get_random_and_build_set():
    global DICTIONARY
    lines = linecache.getlines(WORD_DB)
    for word in lines:
        DICTIONARY.add(word.strip())
    rand_num = random.randrange(1, DB_SIZE)
    master_word = lines[rand_num]
    return master_word.strip(), rand_num


WORD_DB = 'word_db.txt'
DB_SIZE = 12879
WORD_LEN = 5
NUM_GUESSES = 6
GRID_COLS = WORD_LEN
FRAMES = []
CUR_ROW = 0
CUR_COL = 0
EMPTY = '  '
WORDS = [[EMPTY for _ in range(WORD_LEN)] for _ in range(NUM_GUESSES)]
DICTIONARY = set()
MASTER, WORD_NUM = get_random_and_build_set()
print("WORD IS ", WORD_NUM)


def handle_keypress(event):
    """Print the character associated to the key pressed"""
    global CUR_ROW, CUR_COL, FRAMES, MASTER, WORDS, DICTIONARY, EMPTY
    letter = str(event.char).upper()
    update_word_frames(WORDS, FRAMES, CUR_ROW, CUR_COL, letter)
    CUR_COL += 1
    if CUR_COL == 5:
        guess = (''.join(WORDS[CUR_ROW])).lower()
        if guess == MASTER:
            for frame, label in FRAMES[CUR_ROW]:
                frame['background'] = 'green'
        elif guess not in DICTIONARY:
            for col, _ in enumerate(FRAMES[CUR_ROW]):
                update_word_frames(WORDS, FRAMES, CUR_ROW, col, EMPTY)
        else:
            master_set = set(MASTER)
            for i in range(WORD_LEN):
                frame, _ = FRAMES[CUR_ROW][i]
                if guess[i] == MASTER[i]:
                    frame['background'] = 'green'
                elif guess[i] in master_set:
                    frame['background'] = 'yellow'
                else:
                    frame['background'] = 'grey'
                # master_set.remove(guess[i])
            CUR_ROW += 1
            if CUR_ROW == 6:
                print("GAME OVER! out of turns")
        CUR_COL = 0


def update_word_frames(words, frames, row, col, letter):
    words[row][col] = letter
    frame, label = frames[row][col]
    label.config(text=letter)


def delete_letter(event):
    global CUR_ROW, CUR_COL, FRAMES, WORDS, EMPTY
    CUR_COL -= 1
    update_word_frames(WORDS, FRAMES, CUR_ROW, CUR_COL, EMPTY)


def main():
    global FRAMES
    window = tk.Tk()
    window.title("Wordle")
    for i in range(26):
        window.bind(f"{chr(97+i)}", handle_keypress)
    window.bind("<BackSpace>", delete_letter)
    for i in range(NUM_GUESSES):
        word_frames = []
        window.columnconfigure(i, weight=1, minsize=30)
        window.rowconfigure(i, weight=1, minsize=40)
        for j in range(GRID_COLS):
            frame = tk.Frame(
                master=window,
                relief=tk.RIDGE,
                borderwidth=5
            )
            frame.grid(row=i, column=j)
            label = tk.Label(master=frame, text=EMPTY)
            label.pack()
            word_frames.append((frame, label))
        FRAMES.append(word_frames)
    window.mainloop()


if __name__ == '__main__':
    main()


