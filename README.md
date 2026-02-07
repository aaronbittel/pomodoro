# Pomodoro

Minimal Pomodoro Timer TUI written in Python using curses.

- Work duration and pause duration can be customized via command-line arguments:
    + `--work-time` → work duration in minutes (default: 25)
    + `--pause-time` → pause duration in minutes (default: 5)
- Displays a big ASCII timer in the terminal.
- Supports pause/resume and quitting (space to pause/resume, q to quit).

## Example Timer Screen

![Pomodoro Timer Screenshot](assets/pomodoro.png)

## Usage

```bash
git clone https://github.com/aaronbittel/pomodoro
cd pomodoro
uv run pomodoro [--work-dur <minutes>] [--pause-dur <minutes>]
```
