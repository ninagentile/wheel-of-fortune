# Wheel of Fortune

This repository contains a simple **Python implementation of the Wheel of Fortune game**.

## Requirements

To run the game you need:

- **Python** installed on your computer

## Setup

Before running the game, you need to configure two files.

### 1. Add the phrases to guess

Open the file `phrases.py` and insert the phrases that will be used in the game.

A phrase should be written like this:

```python
phrases = [
    Phrase(title='Colombo', phrase_to_guess="Scopre l'America"),
    Phrase(title='Italia', phrase_to_guess='Ha la bandiera tricolore'),
]
```
where:
- `title` is the category or hint
- `phrase_to_guess` is the phrase that players have to guess

### 2. Add the players
Open the file `main_with_players.py` and write the names of the players in the appropriate section of the file.

### 3. Run the game
After configuring the phrases and the players, start the game by running in Bash:
```python
python main_with_players.py
```
