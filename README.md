# Python 2 projects
These projects rely on a third-party library called simplegui. In order to avoid installing Python 2 and simplegui, I recommend copying the LINK (given at the top of each project) and pasting it to Google Chrome. Then, you will see the same code stored in the drive of Codeskulptor, an online Python-2 interpreter.

## Important!
For games to run properly, exit the full-screen mode in Chrome before clicking on the run button (at the top-left corner).

## Rice Rocks
In this mini-project, I built a 2D space game Rice Rocks that is inspired by the classic arcade game Asteroids (1979). Asteroids is a relatively simple game by today's standards, but it was immensely popular during its time. In the game, a player controls a spaceship via four buttons: two buttons that rotate the spaceship clockwise or counterclockwise (independent of its current velocity), a thrust button that accelerates the ship in its forward direction, and a fire button that shoots missiles. Large asteroids spawn randomly on the screen with random velocities. The player's goal is to destroy these asteroids before they strike the player's ship.

* The left and right arrows control the orientation of the spaceship. 

* The up arrow controls the thrusters of the spaceship. When thrusting, the ship accelerates forward.

* When you press the spacebar, the spaceship shoots a missile.

## 2048
2048 is a simple grid-based numbers game. Although the original game is played on a 4x4 grid, this version can handle an arbitrary height and width.

On each turn, a player may slide all of the tiles on the board in one direction (left, right, up, or down). When the player does so, all of the tiles on the board slide as far as they can go in the given direction leaving no empty squares between the tiles. Further, if two tiles of the same number end up next to each other, they merge to form a new tile with twice the value. If no tiles would slide or combine in a given direction, then that is not a legal move, and the player cannot make that move on the current turn.

## Cookie Clicker
Cookie Clicker is a game built around a simulation in which your goal is to bake as many cookies as fast as possible. The main strategy component of the game is choosing how to allocate the cookies that you have produced to upgrade your ability to produce even more cookies faster. 

In Cookie Clicker, you have many options for upgrading your ability to produce cookies. Originally, you can only produce cookies by clicking your mouse. However, you can use the cookies you earn to buy other methods of producing cookies (Grandmas, farms, factories, etc.). Each production method increases the number of "cookies per second" (CPS) you produce. Further, each time you buy one of the production methods, its price goes up. So, you must carefully consider the cost and benefits of purchasing a production method, and the trade-offs change as the game goes on.

This project builds a simple Cookie Clicker class and compares the performance of 4 different strategies:

1) strategy_cursor_broken: this simple strategy always picks "Cursor" no matter what the state of the game is.

2) strategy_cheap: this strategy always selects the cheapest item that you can afford in the time left.

3) strategy_expensive: this strategy always selects the most expensive item you can afford in the time left.

4) strategy_best: this strategy buys the item offering the best CPS-per-unit-of-cost ratio.

## Zombie Apocalypse
In this mini-project, I created a simulation of zombies and humans interacting on a grid. As in the movies, our zombies are hungry for human brains. As a result, zombies chase humans, and humans flee from zombies. In this simulation, zombies are not very agile and can only move up, down, left, or right. On the other hand, humans are more agile and can move in these four directions as well as in the four neighboring diagonal directions.

After running the project, you can add obstacles (black squares), zombies (red squares), and humans (green squares) by first choosing the right option using the "Mouse click" button and then choosing a position on the grid with your mouse.

The "Zombies stalk" button moves zombies towards humans, while the "Humans flee" button moves humans away from zombies. Under the hood, both these buttons use bread-first-search (BFS).

## Pong
Pong is one of the first arcade video games (1972). While Pong is not particularly exciting compared to today's video games, Pong is relatively simple to build and provides a nice opportunity for beginners to work on their programming skills.

This repository contains two files, PongInitial.py and PongOOP.py, both of which are an implementation of Pong. The first file is my initial version of Pong, and the second one is the same project re-written fully using object-oriented programming.

## Memory
Memory is a card game in which a player deals out a set of cards face down. In Memory, a turn (or a move) consists of the player flipping over two cards. If they match, the player leaves them face up. If they don't match, the player flips the cards back face down. The goal of Memory is to end up with all of the cards flipped face up in the minimum number of turns. For this project, I used numbers, but it is also possible to use images or letters in this game. A Memory deck consists of eight pairs of matching cards.

## Word Wrangler
This game takes an input word and then generates all valid words that can be created using the letters in the input word. Possible valid words a taken from this [dictionary](http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt).
