import importlib.util
from pathlib import Path


def test_run_script_can_be_loaded_standalone():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "src/data generation"
        / "run.py"
    )

    spec = importlib.util.spec_from_file_location("run_script", script_path)
    module = importlib.util.module_from_spec(spec)

    assert spec is not None
    assert spec.loader is not None

    spec.loader.exec_module(module)
    assert hasattr(module, "main")
