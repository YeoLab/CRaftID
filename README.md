# CRaftID
Software and code associated with CRaftID Paper

![logo](https://raw.githubusercontent.com/ecwheele/CRaftID/master/logo/Monkee_rafting.png?token=AC2UEILVLNSJNCUQ4RTE3V25XTEOI)


# Hardware requirements:


# Install Instructions:

For targeted_sequencing_analysis and image_processing, refer to the environment YAML file included in this repository. Or create an environment with minimal requirements (Takes a few minutes to install):
```bash
conda create -n CRaftID_paper_py3 -c conda-forge \
  python=3.6.8 biopython opencv=3.4.1 ipykernel tqdm
conda activate CRaftID_paper_py3
python -m ipykernel install --user --name CRaftID_paper_py3 --display-name "CRaftID"
```
For neural network classifier, refer to the ```neural_net_classifier``` README.md, or create an environment with minimal requirements:
### IF USING GPUs:
```bash
conda create -n nn_classifier_gpu -c conda-forge -c anaconda \
  opencv tqdm scikit-learn keras-gpu
conda activate nn_classifier_gpu
```
### IF USING CPU only:
```bash
conda create -n nn_classifier -c conda-forge -c anaconda \
  opencv tqdm scikit-learn keras
conda activate nn_classifier_gpu
```

# Usage:

Refer to the notebooks within each section:
- targeted_sequencing_analysis
- image_processing
- neural_net_classifier

Runtime is not more than a few minutes total for the single image dataset provided here. 