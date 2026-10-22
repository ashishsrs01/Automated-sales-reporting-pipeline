"""Command-line entry point for the sales reporting pipeline."""

from src.reporting.run import generate_report

if __name__ == "__main__":
    print(f"Report generated: {generate_report()}")
