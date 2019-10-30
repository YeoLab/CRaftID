# 0) Install Instructions
## If using anaconda (recommended), install the following packages
conda install -c conda-forge opencv

conda install -c conda-forge tqdm

conda install -c anaconda scikit-learn

### IF USING GPUs:
conda install -c anaconda keras-gpu

### IF USING CPU only:
conda install -c anaconda keras


## If using pip, install the following packages

pip install opencv-python

pip install tqdm

pip install -U scikit-learn

### IF USING GPUs:
pip install tensorflow-gpu

### IF USING CPU only:
pip install tensorflow

pip install Keras

# 1) Deploy the model and classify CellRaft images

To understand how to deploy our model (or your own equivalent model), follow along the notebook titled "Implementation_of_Classifiers.ipynb". This notebook runs through a few example images hosted on this repo, returning their predicted classification. However, when running through the entire dataset of CellRaft images, we used a script with the same code to run in the background.

### Note:

While training the models is best done on GPU instances, this is not necessary for deploying the model. To save on data storage costs, you can deploy and run the model on the computer/compute-cluster hosting your full CellRaft dataset as long as the necessary dependencies can be installed on the system.

# 2) Train your own model or transfer learn from ours

Create a folder with directories inside for each class. Manually curate your training dataset and keep images in these folders as per their assigned class. Set aside 20% of images in each class for downstream testing of your model. If using limited numbers of training data, you can augment the size of the training dataset by flipping, rotating, and adjusting brightness/contrast of images. 

Follow along the notebook titled "Training_classifiers.ipynb". Please note that this notebook is meant as a guide. You will have to supply your own training data as our training data is not yet hosted.

To use transfer learning to further train our pre-trained model for your specific cell lines/phenotypes, follow along this nifty article for the adjustments you would need to make to our code: https://towardsdatascience.com/keras-transfer-learning-for-beginners-6c9b8b7143e

### Note:
We recommend using computing resources with GPU instances to train the model in a time effective manner. We used NVIDIA P6000 instances available on Paperspace, a cloud computing provider. However, it is possible to train and deploy these models on CPU based instances or even on any modern laptop
