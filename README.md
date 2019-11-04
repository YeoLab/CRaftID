# CRaftID

**Pooled CRISPR/Cas9 screening with image-based phenotyping on microRaft arrays reveals stress granule-regulatory factors**

*Software and code associated with CRaftID Paper*

![logo](https://github.com/YeoLab/CRaftID/blob/master/logo/monkeerows_foremily.gif)


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

**Steps to processing CRAFT-ID Data:**

1) Combine image-stacks and segment individual color channels (saved as tif images) for analysis. 

      This setup will vary depending on the screen being performed. Fiji has all the necessary tools and we recommend using macros to programmatically. The first step in the image_processing section contains the python code used to generate a macro to be run in Fiji.
      
2)  Segment images for individual microwells. 

    Each field of view contains many individual microwells depending on the magnification used for imaging. This step will segment each image on individual microwells and save wells that contain cells into a new folder. These are the individual colony images that will be considered for phenotypic analysis. The second step of the image_processing section contains information on how to implement this code. 
    
3)  Filter out unwanted images with neural-network classification. 

    To remove dying colonies and unwanted cellular debris artifacts, we implemented a neural network classifier trained on cell nuclei staining of manually curated images. Instructions to implement the same classification stufy used here are included in the neural_net_classifier section. This will generate a list of images that should be removed from the final analysis. 
    
4) Cell Profiler analysis. 

    Analyze your phenotype of interest with CellProfiler. 
    
  

Refer to the notebooks within each section:
- targeted_sequencing_analysis
- image_processing
- neural_net_classifier

Runtime is not more than a few minutes total for the single image dataset provided here. 
