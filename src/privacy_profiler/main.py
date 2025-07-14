import logging
import argparse
from pathlib import Path
from privacy_profiler.interface.rootview import RootViewController as RootView
from privacy_profiler.model.model import Model
from privacy_profiler.presenter.presenter import Presenter
from privacy_profiler.reporting.report_builder import ReportBuilder 


def setup_logging(log_level: str) -> None:
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler('info.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Privacy Profiler CLI")
    parser.add_argument('--input', '-i', required=True, help="Path to input file (.csv, .parquet, .xlsx, .json)")
    parser.add_argument('--output-format', '-o', default='text', choices=['text', 'json'], help="Format of output")
    parser.add_argument('--output-path', help="If set, saves JSON results to this path")
    parser.add_argument('--verbose', action='store_true', help="Print metric definitions before results")
    parser.add_argument('--log-level', default='INFO', help="Logging level (DEBUG, INFO, WARNING, ERROR)")


    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.log_level)

    logging.debug("Program started with arguments: %s", args)

    model = Model()
    view = RootView(output_format=args.output_format)
    presenter = Presenter(model, view, input_path=args.input)
    results = presenter.run()

    if not results or "metrics" not in results or "interpretation" not in results:
        logging.error("No results to write — exiting.")
        return

    if args.output_path and args.output_format == 'json':
        input_stem = Path(args.input).stem
        output_dir = Path(args.output_path).parent if args.output_path else Path("data-output")
        output_base = output_dir / input_stem

        # Write raw metrics
        metrics_path = f"{output_base}_metrics.json"
        ReportBuilder(str(output_base) + "_metrics.json").write_json(results["metrics"])
        logging.info(f"Metrics JSON written to {metrics_path}")

        # Write interpretation only
        interpretation_path = f"{output_base}_interpretation.json"
        ReportBuilder(str(output_base) + "_interpretation.json").write_json(results["interpretation"])
        logging.info(f"Interpretation JSON written to {interpretation_path}")

        # Write combined full output
        full_path = f"{output_base}_full.json"
        combined = {
            col: {
                **results["metrics"].get(col, {}),
                **results["interpretation"].get(col, {})
            }
            for col in results["metrics"]
        }
        ReportBuilder(str(output_base) + "_full.json").write_json({
            "metrics":combined,
            "row_risk_summary": results["row_risk_summary"]
        })
        logging.info(f"Full JSON output written to {full_path}")
    

    # Write flat CSV report
    csv_path = f"{output_base}_report.csv"
    ReportBuilder(str(output_base) + "_report.csv").write_csv(results["metrics"], results["interpretation"])
    logging.info(f"CSV output written to {csv_path}")

    

    if args.verbose:
        print("\nMetric Reference:")
        print("- gini_coefficient: Measures inequality in distribution (0 = equal, 1 = very skewed)")
        print("- shannon_entropy: Measures diversity and unpredictability in values")
        print("- uniqueness_ratio: Proportion of unique values (1.0 = all unique)")
        print("- null_ratio: Proportion of missing values")
        print()
    

if __name__ == '__main__':
    main()
