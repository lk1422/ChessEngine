#Chess Engine

Using  Neural Network to map a position to a score, probability of white winning from a given position, 
in order to use the minimax algorithm to decide a next best move.

![image](https://user-images.githubusercontent.com/35120812/194970298-0d04951b-023e-4817-afc3-0c2faa537e25.png)

The data was scraped from https://pgnmentor.com/

The goal of the dataset was to take in a position from a grand master game and find the probability of a given player winning.

We also experimented with using convolution neural networks to score the board seperating each piece into a different dimension.

The network is able to preform basic offensive and defensive tactics, but struggles to understand the value of pieces, often trading high value pieces in return for getting check. 

