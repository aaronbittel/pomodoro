import argparse
from datetime import timedelta


def parse_args():
    def minutes_to_timedelta(value: str) -> timedelta:
        """Convert a string number of minutes to timedelta."""
        try:
            minutes = int(value)
            if minutes <= 0:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid positive integer for minutes: {value}"
            )
        return timedelta(minutes=minutes)

    parser = argparse.ArgumentParser(description="Pomodoro timer")
    parser.add_argument(
        "--work-dur",
        type=minutes_to_timedelta,
        default=timedelta(minutes=25),
        help="Work duration in minutes (default: 25)",
    )
    parser.add_argument(
        "--pause-dur",
        type=minutes_to_timedelta,
        default=timedelta(minutes=5),
        help="Pause duration in minutes (default: 5)",
    )

    return parser.parse_args()
