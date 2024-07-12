
jd coins detection - v2 2024-02-19 1:30pm
==============================

This dataset was exported via roboflow.com on July 11, 2024 at 6:32 AM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 5456 images.
Coin are annotated in YOLOv8 format.

The following pre-processing was applied to each image:
* Resize to 640x640 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* 50% probability of horizontal flip
* 50% probability of vertical flip
* Equal probability of one of the following 90-degree rotations: none, clockwise, counter-clockwise
* Random shear of between -10° to +10° horizontally and -10° to +10° vertically
* Salt and pepper noise was applied to 0.1 percent of pixels


