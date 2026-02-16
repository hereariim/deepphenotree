# DeepPhenoTree

[![License GNU LGPL v3.0](https://img.shields.io/pypi/l/deepphenotree.svg?color=green)](https://github.com/hereariim/deepphenotree/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/deepphenotree.svg?color=green)](https://pypi.org/project/deepphenotree)
[![Python Version](https://img.shields.io/pypi/pyversions/deepphenotree.svg?color=green)](https://python.org)
[![tests](https://github.com/hereariim/deepphenotree/workflows/tests/badge.svg)](https://github.com/hereariim/deepphenotree/actions)
[![codecov](https://codecov.io/gh/hereariim/deepphenotree/branch/main/graph/badge.svg)](https://codecov.io/gh/hereariim/deepphenotree)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/deepphenotree)](https://napari-hub.org/plugins/deepphenotree)
[![npe2](https://img.shields.io/badge/plugin-npe2-blue?link=https://napari.org/stable/plugins/index.html)](https://napari.org/stable/plugins/index.html)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)

Herearii Metuarea, Abdoul djalil Ousseni hamza, Walter Guerra† ,  Andrea Patocchi, Lidia Lozano,  Shauny Van Hoye,  Francois Laurens, Jeremy Labrosse,  Pejman Rasti,  David Rousseau† 

† project lead

<img width="1920"  alt="445202004-4a110408-5854-4e8c-b655-4cb588434b79" src="https://github.com/user-attachments/assets/094464d1-8ce8-474b-8473-4a14973cff47" />

<img width="960" alt="DeepPhenoTree" src="https://github.com/user-attachments/assets/ec26e2bf-5983-46aa-8f16-b01e2fdc84a9" />


DeepPhenoTree is though as a tool to enable automatic detection of phenological stages associated with flowering, fruitlet, and fruit in harvest time from images using deep learning–based object detection models.

This [napari] plugin was generated with [copier] using the [napari-plugin-template] (None).

### Contribution

### Article (Draft)

*DeepPhenoTree – Apple Edition: a Multi-site apple phenology RGB annotated dataset with deep learning baseline models.*
Herearii Metuarea, Abdoul djalil Ousseni hamza, Walter Guerra,  Andrea Patocchi, Lidia Lozano,  Shauny Van Hoye,  Francois Laurens, Jeremy Labrosse,  Pejman Rasti,  David Rousseau.

### Dataset

Herearii METUAREA, 2026, "DeepPhenoTree - Apple Edition", https://doi.org/10.57745/NORPF1, Recherche Data Gouv, V1

----------------------------------

## Installation

You can install `deepphenotree` via [pip]:

```
pip install deepphenotree
```

If napari is not already installed, you can install `deepphenotree` with **napari** and **Qt** via:

```
pip install "deepphenotree[all]"
```

To install latest development version :

```
pip install git+https://github.com/hereariim/deepphenotree.git
```

GPU is mandatory for time processing and models running (especially RT-DETR). Please visit the official PyTorch website to get the appropriate installation command:
👉 https://pytorch.org/get-started/locally

**Exemple : GPU (CUDA 12.1)**

    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

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

<!-- <img width="1854" height="1048" alt="Screenshot from 2026-01-09 16-38-04" src="https://github.com/user-attachments/assets/385c5867-ffd1-4de0-8bff-2af0ca1d052b" /> -->

<img width="960" src="src/images/Screenshot from 2026-02-16 15-21-37.png" />


### Scheme

<img width="960" alt="scheme" src="https://github.com/user-attachments/assets/6a7827da-a982-405e-b411-3942b2585f4c" />


### Input

User drag and drop RGB image on napari window.

### Process

User click to make inference in image : 
- Flowering : Detect all objects (from BBCH 00 to BBCH 69) from bud developpement to flowering.
- Fruitlet : Detect fruit in developement (from BBCH 71 to 77)
- Fruit : Detect all fruit in harvest time (from BBCH 81 to 89)

### Output

Bounding box displayed in layer Flowering for flowering, Fruitlet for fruitlet and Fruit for fruit.

## Model

DeepPhenoTree consists of a RT-DETR trained on DeepPhenoTree dataset. 

The trained models used in this project are **not publicly available**. They are part of ongoing research and collaborative projects, and therefore cannot be distributed at this time.  
However, the codebase is provided to ensure **reproducibility** and **transparency** of the proposed methodology.

### Images results

**Metrics are reported as mean ± standard deviation across folds.**

| Dataset   | Location      | Precision       | Recall          | mAP@0.5        | mAP@0.5:0.95   |
|-----------|---------------|-----------------|-----------------|---------------|---------------|
| Flowering | REFPOP        | 0.69 ± 0.01     | 0.58 ± 0.02     | 0.65 ± 0.02   | 0.37 ± 0.02   |
|           | Switzerland   | 0.73 ± 0.02     | 0.60 ± 0.04     | 0.68 ± 0.03   | 0.40 ± 0.04   |
|           | Belgium       | 0.72 ± 0.02     | 0.63 ± 0.03     | 0.69 ± 0.03   | 0.40 ± 0.03   |
|           | Spain         | 0.66 ± 0.01     | 0.53 ± 0.05     | 0.60 ± 0.03   | 0.30 ± 0.02   |
|           | Italy         | 0.69 ± 0.04     | 0.61 ± 0.03     | 0.67 ± 0.04   | 0.40 ± 0.04   |
| Fruitlet  | REFPOP        | 0.85 ± 0.02     | 0.73 ± 0.02     | 0.82 ± 0.02   | 0.53 ± 0.01   |
|           | Switzerland   | 0.86 ± 0.04     | 0.78 ± 0.04     | 0.84 ± 0.06   | 0.56 ± 0.04   |
|           | Belgium       | 0.83 ± 0.03     | 0.65 ± 0.04     | 0.77 ± 0.04   | 0.52 ± 0.14   |
|           | Spain         | 0.86 ± 0.02     | 0.72 ± 0.03     | 0.81 ± 0.03   | 0.52 ± 0.03   |
|           | Italy         | 0.88 ± 0.01     | 0.80 ± 0.01     | 0.88 ± 0.01   | 0.61 ± 0.01   |

## DeepPhenoTree Dataset

DeepPhenoTree – Apple Edition, a multi-site, multi-variety,  RGB  image  dataset  dedicated  to  the  classification  of  key  apple  treephenological stages.

<img width="1920" height="1080" alt="IRTA_time" src="https://github.com/user-attachments/assets/9eae80e6-73e1-45ad-b5e5-70a41807301b" />


## Acknowlegments

We would like to thank the following people for their contributions to the project: Herearii Metuarea, Abdoul-Djalil Ousseini Hamza, Lou Decastro, Jade Marhadour, Oumaima Karia, Lorène Masson, Marie Kourkoumelis-Rodostamos, Abdoul-Djalil Hamza Ousseinni, Walter Guerra, Francesca Zuffa, Francesco Panzeri,  Andrea Patocchi, Lidia Lozano,  Shauny Van Hoye,  Francois Laurens, Jeremy Labrosse,  Pejman Rasti,  David Rousseau.

## Contact

Imhorphen team, bioimaging research group
42 rue George Morel, Angers, France

- Herearii Metuarea, herearii.metuarea@univ-angers.fr
- Abdoul-Djalil Ousseini Hamza, abdoul-djalil.ousseini-hamza@inrae.fr
- Pr David Rousseau, david.rousseau@univ-angers.fr

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [GNU LGPL v3.0] license,
"deepphenotree" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

## Citing

If you use DeepPhenoTree code or dataset in your research, please use the following BibTeX entry.

```
Not available
```

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
