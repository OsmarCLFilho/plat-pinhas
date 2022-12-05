.. Plat Pinhas documentation master file, created by
   sphinx-quickstart on Mon Dec  5 00:10:16 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Plat Pinhas's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

About the Game
--------------

Plat Pinhas is a game project written in Python, with extensive use of the Pygame library. It aims to go beyond the library's intended use by rendering a game in 3D graphics, although not perfectly due to approximations in its methods. It is comprised of a infinite, procedurally generated, plataform jumper, with a roguelike aproach to its shop system, where after each death the player may buy better characters.

Player's Objectives
-------------------

Primarily, the player must survive by jumping onto the newly created platforms, as all of them have an expiration time. The longer the player survives, the more points they will acquire in their death, allowing them to buy new characters. Ultimately, the final character, "Emapon" is the end object of the game. It has overly tuned stats and a double jump ability. This allows the player to experience the final levels of platform decay, as the expiration timers get shorter and shorter as the game progresses.

Controls
--------

The controls follow the mainstream convention of foward/backward movement by the W and S keys, left/right movement by the A and D keys, jumping by the space key and camera control by mouse movement. Characters can jump a set amount of times, independently of touching the ground. However, while doing so, their jump count is reset. This happens both over horizontal and vertical surfaces, allowing for wall jumping and climbing.

The Rendering
-------------

The process of rendering the 3D scenario is done by ``render.py``. By taking in a ``Space`` object from ``game.py``, it goes through all of its ``Body`` objects and calculates how should each vertex and triangle be projected into the camera ``Camera`` object. It then orders all the resulting 2D triangles so that the closest objects get drawn last and returns this list of triangles to ``game.py``.

Platform Generation
-------------------

Given a starting platform, placed right below the player at the beginning of the game, a vector is used to determine the next plataform's location. This vector can receive random noise to vary its direction. It can also be sharply turned in rare ocassions, resulting in 90 degree turns in the path of platforms.

There are 3 kinds of platforms: static, flat ones; static, tall ones and; moving, flatones.

Each plataform has a timer. The starting time of a timer is determined by the amount of points collected so far by the player, the more points, the shorter the starting time. Once a timer reaches 0, its platform is deleted.

Character Stats
---------------

The things are differentiate the characters from one another, other than their sprites, are their stats. These are: jump strength, maximum number of jumps and speed.

The Shop
--------

The shop is the section of the menu where you can acquire new characters. After you end a run, the main menu is brought back up and the player can choose to view the shop. There, you may buy and select which character you want to use in your next run. After buying a character, it doesn't get automatically selected.
