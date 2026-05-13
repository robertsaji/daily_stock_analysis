#!/usr/bin/env python3
"""
Daily Stock Analysis - Main Entry Point

This module serves as the primary entry point for the daily stock analysis tool.
It orchestrates data fetching, analysis, and report generation.
"""

import os
import sys
import logging
import argparse
from datetime import datetime, date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"logs/analysis_{date.today().strftime('%Y%m%d')}.log"),
    ],
)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for the stock analysis tool."""
    parser = argparse.ArgumentParser(
        description="Daily Stock Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --symbols AAPL TSLA MSFT
  python main.py --symbols AAPL --date 2024-01-15
  python main.py --config config.yaml --output reports/
        """,
    )

    parser.add_argument(
        "--symbols",
        nargs="+",
        default=None,
        help="Stock ticker symbols to analyze (e.g., AAPL TSLA MSFT)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=date.today().strftime("%Y-%m-%d"),
        help="Analysis date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.getenv("OUTPUT_DIR", "reports"),
        help="Output directory for analysis reports",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose/debug logging",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Run analysis without saving output files",
    )

    return parser.parse_args()


def setup_directories(output_dir: str) -> None:
    """Ensure required directories exist."""
    directories = [output_dir, "logs", "data/cache"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Directory ensured: {directory}")


def run_analysis(args: argparse.Namespace) -> int:
    """
    Main analysis pipeline.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    logger.info(f"Starting daily stock analysis for date: {args.date}")
    logger.info(f"Target symbols: {args.symbols or 'from config'}")

    try:
        setup_directories(args.output)

        # TODO: Initialize components as they are built
        # from analysis.fetcher import StockDataFetcher
        # from analysis.analyzer import StockAnalyzer
        # from analysis.reporter import ReportGenerator

        logger.info("Analysis pipeline completed successfully.")
        return 0

    except KeyboardInterrupt:
        logger.warning("Analysis interrupted by user.")
        return 130
    except Exception as e:
        logger.error(f"Analysis failed with error: {e}", exc_info=True)
        return 1


def main() -> None:
    """Application entry point."""
    args = parse_arguments()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled.")

    if args.dry_run:
        logger.info("[DRY RUN] No files will be written.")

    exit_code = run_analysis(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
