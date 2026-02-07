import curses
from datetime import datetime, timedelta
from enum import Enum, auto
from dataclasses import dataclass

from pomodoro.args import parse_args
from pomodoro.ascii import big_ascii

FPS = 30
BLOCKING = -1


class AppState(Enum):
    Idle = auto()
    Running = auto()
    Paused = auto()
    Done = auto()


def main() -> None:
    args = parse_args()
    curses.wrapper(_main, args.work_dur, args.pause_dur)


def centered(stdscr: curses.window, msg: str | list[str]) -> None:
    height, width = stdscr.getmaxyx()
    if isinstance(msg, str):
        y, x = height // 2, width // 2 - len(msg) // 2
        stdscr.addstr(y, x, msg)
    elif isinstance(msg, list):
        text_height = len(msg)
        text_width = max(len(row) for row in msg)
        y = height // 2 - text_height // 2
        x = width // 2 - text_width // 2
        for i, line in enumerate(msg):
            stdscr.addstr(y + i, x, line)


def duration_to_str(dur: timedelta) -> str:
    if dur.days > 0:
        raise ValueError("Duration cannot be longer than 24 hours (days must be 0).")
    if dur.seconds / 60 > 99:
        raise ValueError("Duration cannot exceed 99 minutes.")
    minutes, seconds = divmod(dur.seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


@dataclass
class PomodoroTimer:
    start_time: datetime | None = None
    end_time: datetime | None = None
    remaining_duration: timedelta | None = None

    def start(self, duration: timedelta) -> None:
        self.start_time = datetime.now()
        self.duration = duration
        self.end_time = self.start_time + self.duration
        self.remaining_duration = duration

    def pause(self) -> None:
        self.remaining_duration = self.remaining()

    def unpause(self) -> None:
        if self.remaining_duration is None:
            raise RuntimeError("Cannot unpause timer: timer has not been started yet.")
        self.start_time = datetime.now()
        self.end_time = self.start_time + self.remaining_duration

    def remaining(self) -> timedelta:
        if self.end_time is None:
            raise RuntimeError(
                "Cannot get remaining time: timer has not been started yet."
            )
        return self.end_time - datetime.now()


def _main(stdscr: curses.window, work_dur: timedelta, pause_dur: timedelta) -> None:
    curses.curs_set(0)

    appstate = AppState.Idle
    show = True
    is_work_time = True

    timer = PomodoroTimer()

    centered(stdscr, big_ascii(duration_to_str(work_dur)))
    height, width = stdscr.getmaxyx()
    footer = f"Current State: {appstate}"
    stdscr.addstr(height - 1, width // 2 - len(footer) // 2, footer)

    while True:
        key = stdscr.getch()
        stdscr.refresh()
        stdscr.erase()

        if key == ord("q"):
            break
        if key == ord("b"):
            curses.beep()
        elif key == ord(" "):
            if appstate == AppState.Idle:
                appstate = AppState.Running
                timer.start(work_dur if is_work_time else pause_dur)
                stdscr.timeout(FPS)
            elif appstate == AppState.Running:
                appstate = AppState.Paused
                timer.pause()
            elif appstate == AppState.Paused:
                appstate = AppState.Running
                timer.unpause()
                stdscr.timeout(FPS)
            elif appstate == AppState.Done:
                is_work_time = not is_work_time
                appstate = AppState.Idle

        if appstate == AppState.Idle:
            duration = work_dur if is_work_time else pause_dur
            centered(stdscr, big_ascii(duration_to_str(duration)))
        elif appstate == AppState.Running:
            remaining = timer.remaining()
            if remaining <= timedelta():
                appstate = AppState.Done
                stdscr.timeout(500)
            else:
                centered(stdscr, big_ascii(duration_to_str(timer.remaining())))
        elif appstate == AppState.Paused:
            centered(stdscr, big_ascii(duration_to_str(timer.remaining())))
            stdscr.timeout(BLOCKING)
        elif appstate == AppState.Done:
            if show:
                centered(stdscr, big_ascii("00:00"))
            show = not show

        height, width = stdscr.getmaxyx()
        footer = f"Current State: {appstate}"
        stdscr.addstr(height - 1, width // 2 - len(footer) // 2, footer)

    curses.curs_set(1)


if __name__ == "__main__":
    main()
