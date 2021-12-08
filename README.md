# Mini-Project 2 Game of Line 'em Up

https://github.com/efeharmankaya/mp2-comp472

## MP2 Artificial Intelligence COMP 472
Line 'em Up is a generic version of tic-tac-toe: it is an adverserial 2 player game played on a nxn board with the possible values:
<table>
    <thead>
        <th>
            white piece
        </th>
        <th>
            black piece
        </th>
        <th>
            bloc
        </th>
        <th>
            empty position
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                ○
            </td>
            <td>
                ●
            </td>
            <td>
                ⛝
            </td>
            <td>
                □
            </td>
        </tr>
    </tbody>
</table>

The project implements an adversarial search using minimax or alphabeta functions. The game of an nxn board can be played with a human player through the console or fully automated. Two heuristic functions were developed to experiment with the trade-offs between execution time and the quality of the piece estimate.

## Trace Files
For each game played a full trace file will be created with the name gametrace-nbst.txt where n = n in nxn, b = number of blocs, s = number of consecutive pieces to win, t = max time required for AI to return a move

If run through the function run() in line_em_up.py (ln: 630) an automated scoreboard file will be generated with the computed average analysis metrics for each iteration of games.
## Setup environment
```bash
..\>pip3 install numpy
```

## Running the Experiements
The current setup of the main function is to run a series of tracked games alternating between heuristics and calculate the average computation metrics, however, to run a manually implemented game, run the main() function instead of the run() function inside of line_em_up.py

```bash
..\>python3 line_em_up.py
```