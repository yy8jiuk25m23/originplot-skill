r"""Optional Windows-only builder for a DATA-ONLY editable Origin project.

This script has NOT been executed in Origin in the Linux analysis environment.
It imports the actual analysis CSV tables without recalculating/selecting scans.
It does not reconstruct the six graph pages or claim pixel-identical rendering.

Usage on Windows with licensed Origin installed:
  py -m pip install originpro==1.1.15 pandas numpy
  py build_origin_data_project.py --data-dir ..\data --output ICP_sensitivity_data.opju

The APIs used were checked against the published originpro 1.1.15 source.
"""
from __future__ import annotations
import argparse
import json
import platform
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', required=True, type=Path,
                        help='Directory containing the actual analysis CSV files (searched recursively).')
    parser.add_argument('--output', required=True, type=Path,
                        help='New data-only Origin project path, ending in .opju; must not already exist.')
    args = parser.parse_args()
    if platform.system() != 'Windows':
        parser.exit(2, 'Requires Windows Python and a local licensed Origin installation. No project was generated.\n')
    if args.output.suffix.lower() != '.opju':
        parser.error('--output must end in .opju')
    if args.output.exists():
        parser.error('Refusing to overwrite an existing project. Choose a new output path.')
    csvs = sorted(args.data_dir.resolve().rglob('*.csv'))
    if not csvs:
        parser.error('No CSV data tables found under --data-dir')
    import pandas as pd
    import originpro as op

    # A new project intentionally owns this external Automation session.
    # The caller should close other unsaved Origin sessions before executing.
    op.set_show(True)
    op.new()
    imported = []
    for csv in csvs:
        df = pd.read_csv(csv, keep_default_na=False)
        sheet = op.new_sheet('w', lname=csv.stem)
        if sheet is None:
            raise RuntimeError(f'Origin failed to create a worksheet for {csv}')
        sheet.from_df(df, addindex=False)
        imported.append({'source_csv': str(csv), 'rows': len(df),
                         'columns': [str(c) for c in df.columns]})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    saved = op.save(str(args.output.resolve()))
    if not saved or not args.output.is_file() or args.output.stat().st_size == 0:
        raise RuntimeError('Origin did not confirm a nonempty saved project.')
    log = {'status': 'Saved by actual Windows Origin Automation',
           'project_kind': 'data-only editable worksheet project; six graph pages are not reconstructed',
           'output': str(args.output.resolve()), 'imported_tables': imported,
           'normalization_or_filtering_in_this_builder': 'none; source CSV values imported unchanged'}
    args.output.with_suffix('.import_log.json').write_text(json.dumps(log, indent=2), encoding='utf-8')
    print(f'Saved editable data project: {args.output.resolve()}')
    print('Origin remains open. This builder does not create or replace the supplied six final figures.')


if __name__ == '__main__':
    main()
