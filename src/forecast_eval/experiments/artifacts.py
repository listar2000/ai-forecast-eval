import hashlib
import json
import platform
import subprocess
from importlib.metadata import version
from pathlib import Path
import numpy as np
from .. import __version__


def clean(value):
    if isinstance(value, np.ndarray):
        return clean(value.tolist())
    if isinstance(value, np.generic):
        return clean(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return None
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    return value


def dumps(value):
    return json.dumps(clean(value), allow_nan=False, sort_keys=True)


def metadata():
    root = Path(__file__).resolve().parents[3]
    hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((root / 'src').rglob('*.py'))}
    def git(*args):
        try:
            return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.DEVNULL, text=True).strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
    return {'package_version': __version__, 'python': platform.python_version(),
            'platform': platform.platform(), 'dependencies': {p: version(p) for p in ['numpy', 'scipy', 'PyYAML']},
            'git_commit': git('rev-parse', 'HEAD'), 'git_status': git('status', '--porcelain'),
            'source_sha256': hashes}


def write_artifacts(output, config, records, summary):
    path = Path(output)
    path.mkdir(parents=True, exist_ok=False)  # never overwrite a previous experiment
    (path / 'config.json').write_text(dumps(config.to_dict()) + '\n')
    (path / 'metadata.json').write_text(dumps(metadata()) + '\n')
    (path / 'replicates.jsonl').write_text(''.join(dumps(r) + '\n' for r in records))
    (path / 'summary.json').write_text(json.dumps(clean(summary), indent=2, allow_nan=False) + '\n')
    return path
