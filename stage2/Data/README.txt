Table A - gamespot.csv (8884 tuples)
Table B - howLongToBeat.csv (8481 tuples)

Both the tables have following 7 attributes:

1) Title        - Name of the video game
2) Developer    - Individuals/Studios who developed the video game
3) Publisher    - Studio who published the video game
4) Platform     - Platform on which video game is available. Example: XBox, PlayStation, Wii
5) Genre        - Genre of the video game. Example: Action, Sports, Puzzle
6) ReleaseDate  - Date on which game was released
7) Rating       - Average user rating on a scale of 10

Other Information:
1) Developer, Publisher, Platform, and Genre attributes can have multiple values for a single game. In case of multiple values, values are delimited by a vertical bar(|) .
2) In Gamspot.csv, first few tuples have Title attribute which looks like ".hack//G.U. vol. 1//Rebirth" . Please note that this is the actual title of a game, and is not a bug in data extraction.