# Bridge - card game

## About 
Multiplayer, online, popular card game - bridge. Connection with server will be established after typing unique username.
Then user can create new table or joining to the existing one. Only 4 empty table can be listed in main menu. When the
table is full, the bidding stage starts. For more information about bridge visit [wikipedia](https://en.wikipedia.org/wiki/Contract_bridge).

## Requirements
- Python
- Pygame

## Controls
### Bidding
You can bid by clicking on the specific bidding box. Firstly pick the level of call, then its suit.
The bidding is over after 3 folds in the row (4 at the beginning). The last bid becomes a final contract.
The player (from winning side), who first names the winning suit becomes declarer. His partner will be dummy.

### Playing
The dummy's hand is exposed on the table after first lead. The declarer plays both himself cards and the dummy's.
The first card played to the trick dictates the suit that others must play (if able to do so). When all cards have been played
the game is over.

## Deployment
I am planning to deploy this game on Google Cloud Virtual Server after a few tests of gameplay.