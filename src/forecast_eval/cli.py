import argparse
import sys
import yaml
from pathlib import Path
from .experiments.config import load_config
from .experiments.runner import run_experiment
from .experiments.artifacts import write_artifacts


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run paired forecasting-ranking simulations')
    parser.add_argument('config', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.output.exists():
            raise ValueError(f'Output already exists: {args.output}')
        config = load_config(args.config)
    except (ValueError, TypeError, OSError, yaml.YAMLError) as exc:
        parser.error(str(exc))
    records, summary = run_experiment(config)
    write_artifacts(args.output, config, records, summary)
    for key, row in summary['methods'].items():
        print(f"{key}: failures={row['fit_failures']}, partial={row['partial_rankings']}")
        for metric in config.metrics:
            item = row['metrics'][metric]
            print(f"  {metric}: {item['mean']} (MCSE {item['mcse']}; n={item['n_valid']})")
    print(f'Results: {args.output.resolve()}')
    return 1 if any(r['status'] != 'ok' for r in records) else 0


if __name__ == '__main__':
    sys.exit(main())
