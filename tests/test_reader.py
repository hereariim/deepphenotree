import importlib.util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
READER_PATH = ROOT / "src" / "deepphenotree" / "_reader.py"


def _load_reader_module():
    spec = importlib.util.spec_from_file_location(
        "test_reader_module", READER_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


# tmp_path is a pytest fixture
def test_reader(tmp_path):
    """An example of how you might test your plugin."""
    reader_module = _load_reader_module()

    # write some fake data using your supported file format
    # we make the array an integer type to be compatible with the reader
    my_test_file = str(tmp_path / "myfile.npy")
    original_data = np.random.rand(20, 20).astype(np.int_)
    np.save(my_test_file, original_data)

    reader = reader_module.napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # make sure it's the same as it started
    np.testing.assert_allclose(original_data, layer_data_tuple[0])


def test_get_reader_pass(tmp_path):
    reader_module = _load_reader_module()
    reader = reader_module.napari_get_reader("fake.file")
    assert reader is None

    # the original_data is a float type, so the reader should return None
    my_test_file = str(tmp_path / "myfile.npy")
    original_data = np.random.rand(20, 20)
    np.save(my_test_file, original_data)

    reader = reader_module.napari_get_reader(my_test_file)
    assert reader is None
