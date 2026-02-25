try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"


from ._reader import napari_get_reader
from ._sample_data import make_sample_data
from ._widget import (
    ThreeButtonsWidget,
)
from .inference import YoloInferencer
from .data_manager import ensure_data


__all__ = (
    "napari_get_reader",
    "make_sample_data",
    "ThreeButtonsWidget",
    "YoloInferencer",
)

from pathlib import Path
package_dir = Path(__file__).resolve().parent
if not (package_dir / "sample_data").exists():
    ensure_data()