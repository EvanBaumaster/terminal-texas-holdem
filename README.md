Terminal Texas Hold 'em
What it does
Terminal Texas Hold 'em is a fully functional command-line poker game written entirely in Python. It allows a single human player to compete against up to eight AI opponents in standard No-Limit Texas Hold 'em. The application seamlessly handles deck shuffling, card dealing, complex betting rounds (including folds, calls, raises, and all-ins), and final hand evaluation to determine the winner of the pot.

This project solves the problem of needing a lightweight, fast, and easily accessible way to practice poker strategies or pass the time without the overhead of heavy graphical interfaces or internet connections.

Installation
To run this application, you will need Python 3.8 or higher installed on your system.

Clone this repository to your local machine:

Bash
git clone https://github.com/yourusername/terminal-texas-holdem.git
Navigate into the project directory:

Bash
cd terminal-texas-holdem
Create and activate a virtual environment (recommended):

Bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required dependencies (used for terminal formatting):

Bash
pip install -r requirements.txt
Usage
To start a standard game, simply run the main Python script from your terminal. By default, this will launch a table with 3 AI opponents and a starting stack of 1000 chips for all players.

Bash
python poker.py
Expected Output:
The terminal will clear and display the initial game state, showing your two hole cards, your current chip count, the current pot size, and prompt you for your first action (Fold, Call, or Raise).

Examples
1. Standard Game (Default)
Launch a standard 4-player game with default chip stacks.

Bash
python poker.py
2. Customizing the Table
You can adjust the number of AI opponents and the starting chip stack using command-line flags. This example starts a massive 9-player table with 5,000 starting chips.

Bash
python poker.py --opponents 8 --chips 5000
3. Turbo Mode
If you want to skip the artificial delays between AI betting actions and deal animations, you can use the --fast flag to speed up gameplay.

Bash
python poker.py --fast
Known limitations and future ideas
Limitations: The current AI opponents rely on basic probability thresholds and random number generation rather than advanced machine learning, making them somewhat predictable in long sessions. The application also only supports standard No-Limit rules, with no support for Pot-Limit or Limit variations.

Future Ideas: In the future, I plan to implement a save-state feature so users can pause and resume tournaments. I would also like to add local network multiplayer support using Python's socket library so friends can play against each other from different terminals.
