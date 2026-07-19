"""
main.py
Command-line entry point. Usage:
    python main.py "Toronto"
"""

import sys
from weather import lookup


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py \"City Name\"")
        sys.exit(1)

    city = sys.argv[1]

    try:
        report = lookup(city)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Weather for {report['name']}:")
    print(f"  Condition:  {report['condition']}")
    print(f"  Temp:       {report['temperature_c']}°C")
    print(f"  Wind speed: {report['windspeed_kmh']} km/h")


if __name__ == "__main__":
    main()