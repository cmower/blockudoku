# blockudoku

My PyGame implementation of Blockudoku.

# Gameplay

Blockudoku is a game that mixes ideas from Tetris and Sudoku.
In each turn you place Tetris-like items in non-colliding positions.
When a full column/row or 3-by-3 block (in Sudoku-like locations) are full then they disappear and you can place items in those blocks again.
Each time blocks dissapear, your score goes up and the goal is to get as high score possible until there are no positions left.

# Requirements

* Python 3
* PyGame, install using `$ pip install pygame`

# Run

```
$ cd /path/to/blockudoku
$ python main.py [OPTIONS]
```

Options:
* `--usealtmusic`: play alternative music track
* `--nosound`: music is not played
