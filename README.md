# Peg-Game

I recreated the Cracker Barrel triangle game and programmed an AI to learn to solve it.

The AI is an epsilon reinforcment agent. Sometimes, it decides to take a random action, but the rest of the time, it takes the best known action.
You can alter the alpha, epsilon, and discount values of the agent. Simply run python Main.py --help to learn which variables you can control.
The size of the board is variable. You can make it as large or as small as you like, you just have to specify the row count.
In the initial state, per Cracker Barrel rules, the empty hole always starts at the top.

To run the program with its default values, run python Main.py
You can see which variables you can alter using python Main.py --help
For instance, if you wanted to change the epsilon value of the agent and the number of rows on the board, you would run

python Main.py -e float -r int
