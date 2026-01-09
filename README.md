# deepphenotree

[![License GNU LGPL v3.0](https://img.shields.io/pypi/l/deepphenotree.svg?color=green)](https://github.com/hereariim/deepphenotree/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/deepphenotree.svg?color=green)](https://pypi.org/project/deepphenotree)
[![Python Version](https://img.shields.io/pypi/pyversions/deepphenotree.svg?color=green)](https://python.org)
[![tests](https://github.com/hereariim/deepphenotree/workflows/tests/badge.svg)](https://github.com/hereariim/deepphenotree/actions)
[![codecov](https://codecov.io/gh/hereariim/deepphenotree/branch/main/graph/badge.svg)](https://codecov.io/gh/hereariim/deepphenotree)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/deepphenotree)](https://napari-hub.org/plugins/deepphenotree)
[![npe2](https://img.shields.io/badge/plugin-npe2-blue?link=https://napari.org/stable/plugins/index.html)](https://napari.org/stable/plugins/index.html)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)

DeepPhenoTree is though as a tool to enable automatic detection of phenological stages associated with flowering, fruitlet, and fruit in harvest time from images using deep learning–based object detection models.

This [napari] plugin was generated with [copier] using the [napari-plugin-template] (None).

## Article

*DeepPhenoTree – Apple Edition: a Multi-site apple phenology RGB annotated dataset with deep learning baseline models.*
Herearii Metuarea, Walter Guerra,  Andrea Patocchi, Lidia Lozano,  Shauny Van Hoye,  Francois Laurens, Jeremy Labrosse,  Pejman Rasti,  David Rousseau.

<img width="1920" height="165" alt="445202004-4a110408-5854-4e8c-b655-4cb588434b79" src="https://github.com/user-attachments/assets/094464d1-8ce8-474b-8473-4a14973cff47" />

----------------------------------

## Installation

You can install `deepphenotree` via [pip]:

```
pip install deepphenotree
```

If napari is not already installed, you can install `deepphenotree` with napari and Qt via:

```
pip install "deepphenotree[all]"
```

To install latest development version :

```
pip install git+https://github.com/hereariim/deepphenotree.git
```
## Getting started

### Running from Python
```
from deepphenotree.inference import YoloInferencer
image = # Your RGB image

# Flowering task
infer = YoloInferencer("Flowering")
bbx = infer.predict_boxes(image)

# Fruitlet task
infer = YoloInferencer("Fruitlet")
bbx = infer.predict_boxes(image)

# Fruit task
infer = YoloInferencer("Fruit")
bbx = infer.predict_boxes(image)
```

### Running from Napari

This plugin is a tool to perform targeted image inference on user-provided images. Users can run three specific detection tasks via dedicated buttons: flowering, fruitlet, and fruit detection. The plugin returns the coordinates of bounding boxes around detected objects, and a message informs the user of the number of detected boxes. Several developments are ongoing—feel free to contact us if you have requests or suggestions.

## Acknowlegments

We would like to thank the following people for their contributions to the project: Herearii Metuarea, Walter Guerra,  Andrea Patocchi, Lidia Lozano,  Shauny Van Hoye,  Francois Laurens, Jeremy Labrosse,  Pejman Rasti,  David Rousseau, Abdoul-Djalil Hamza Ousseinni, Francesca Zuffa, Francesco Panzeri, Lou Decastro, Jade MARHADOUR, Oumaima Karia, Lorène MASSON, Marie Kourkoumelis-Rodostamos.

## Contact

- Herearii Metuarea, PhD Student, Université d'Angers
- Abdoul-Djalil Hamza Ousseini, Engineer, INRAe
- David Rousseau, Full Professor, Université d'Angers

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [GNU LGPL v3.0] license,
"deepphenotree" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[copier]: https://copier.readthedocs.io/en/stable/
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[napari-plugin-template]: https://github.com/napari/napari-plugin-template

[file an issue]: https://github.com/hereariim/deepphenotree/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
