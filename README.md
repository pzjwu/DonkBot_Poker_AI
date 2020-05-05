# DonkBot_Poker_AI
An experiment on singling out various aspects of human poker players to observe behavior

FULL DISCLOSURE: ALL OF THESE AI CANNOT PLAY WELL WHATSOEVER, IF YOU DECIDE TO USE THEM IT'S YOUR MONEY TO LOSE

With that out of the way...

This collection of various Poker AI is meant to highlight and observe performances of various poker strategies and thoughts (Exploitative Play vs GTO Play)

There are 3.5 unique bots (depending on what you consider unique).

The first 2, Monte Carlo and Conte Marlo both use Monte Carlo simulations of an arbitrary amount as proxy calculations for showdown equity.
The Monte Carlo Bot utilizes a GMM (Gaussian Mixture Model) inspired betting strategy of 3 normal distributions to determine action. Sizing is taken from The Grinder's Manual
The Conte Marlo Bot utilizes an honest algorithm. Normally you would think this one sucks, and normally you would be right, but since almost none of these bots exhbit proficient exploitative tendencies as well as all displaying "memorylessness", it works fairly well.

The Heuristic Bot is a set of heuristics (pot odds, implied odds, RFI strategies, three betting ranges,...) taken from The Grinder's Manual. It does well against bots that can somewhat play normally, and gets eaten alive by the fish bot for 2 reasons.
1. It's preflop range is too small, and it gets pwned by blinds and antes. The fish bot exhibits proficient ability against the heuristic bot in realizing fold equity
2. This is an incomplete strategy (the AI bricks if you throw in too many facets to consider)

The Bayesian Bot utilizes a Dynamic Bayesian Network based on opponent positioning, action, sizing, and prior beliefs to perform Bayesian Updating.
It is an uncalibrated bot, with no training, but it works a little bit.

If you're confused why I'm not really quantifying performance, a Jupyter Notebook is available in the Data Folder to observe performance in a Round Robin Tournament.
50 sessions of 200 hands apiece is not that large, and variance still plays a very strong factor.

To Run
If you want to rerun the round robin to generate more hands, change the values in rounds in range(x), as well as max_rounds.
If you want to just run 2+ bots against each other and observe, use other_main.
If you want to play against one using the GUI, change the config file.
