
# Skin Cancer Detector

This repository contains material that is part of Project 4 of Monash University Boot Camps' Data Analytics Bootcamp made by Group 2 - [Nicholas Dale](https://github.com/falconpunch082), [Duc Trieu Pham](https://github.com/Lilydales), [Sohaila Nazari](https://github.com/S-haila) and [Abhidnya](https://github.com/Abhidnya05).

## Project Overview

The purpose of this project is to create a website that hosts a convolutional neural network model that is purpose-built to detect whether a photo provided by an end-user shows signs of common skin cancers like melanoma, basal cell carcinoma or squamous cell carcinoma.

The website is easy to use for everyone, regardless of technological prowess. Users simply click on a button to attach a photo they would like to analyse for skin cancer, and then click another button to see the results. In addition to that, the website also hosts interesting information and infographics about skin cancer that aims to educate people about skin cancer, a cancer that is getting more prevalent as time goes on.

Behind the scenes lies the backbone of the skin cancer detection service - the convolutional neural network HOTARU (Health Observing Technology for Assessing Risks Unveiled) accompanied by the image preprocessing script SPARK (Skin Pattern Analysis and Recognition Kit). SPARK takes in the photo uploaded by the user and modifies it to isolate only the skin spot in question. It then provides the preprocessed image to HOTARU, which goes through every single pixel of the image to determine whether the image shows signs of skin cancer.

## Technologies Used
- Tensorflow
- OpenCV
- Pillow (PIL)
- Numpy
- Scikit Image

## The Website in Action


## Contributions

Nicholas Dale - Machine Learning Engineer (HOTARU and SPARK creator)

Duc Trieu Pham - Website UI, input, model integration and other frontend/backend

Sohaila Nazari - Data Engineer and SPARK collaborator

Adhidnya - Data Engineer and Researcher

## Final Repository Structure


## Launch

There is no need for any kind of installation due to the website being hosted in the Internet.

However, versions of HOTARU and SPARK are available in the repo should one want to load them in a notebook for their own testing purposes.

## Documentation

Every version of HOTARU and SPARK are encased within their respective notebooks. There you will find a breakdown of how they were made, alongside test results. There is a notebook specially made to test v1.1's capabilities with a larger dataset.

There is also a notebook available that shows how SPARK does its magic, one step at a time. In addition, the notebook that is used to separate the raw image data into training, validation and test folders and then process them is available.

Logs are also available, which break down how all models made were created (including ones that did not reach production stage).

Finally, a [progress log](https://github.com/falconpunch082/skin-cancer-detection/blob/nick/HOTARU%20Model%20Creation%20Progress%20Log.docx) is available for a more detailed discussion on how the model was made.

## Data Sources

Pictures showing skin cancers were accumulated from the website https://api.isic-archive.com/collections/70/. We thank the ISIC organisation for the open-source release of the 2018, 2019 and 2020 Challenge datasets.

Pictures not showing skin cancers were handpicked from the following websites:
-	https://www.kaggle.com/datasets/ahmedxc4/skin-ds 
-	https://www.kaggle.com/datasets/ismailpromus/skin-diseases-image-dataset 
-	https://www.kaggle.com/datasets/subirbiswas19/skin-disease-dataset 

## Acknowledgements

We would like to thank [Evan/EdjeElectronics](https://github.com/EdjeElectronics) for making their image data augmentation Python script open-source. It was thanks to them that we were able to create a suitable dataset for HOTARU to learn from. The Python script used is in the repo, but we recommend taking a look at their repo too (https://github.com/EdjeElectronics/Image-Augmentation-Examples-for-Machine-Learning/tree/master).

We would also like to thank our teaching assistant Hamim and lecturer Saaransh for their guidance and feedback during this project.