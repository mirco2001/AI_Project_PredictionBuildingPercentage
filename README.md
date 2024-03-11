# Project Title: Prediction of the construction percentage of a building

## Overview
The goal of this project is to predict the construction percentage of a building based on a series of input images. In particular, both an automatic and manual mechanism has been developed for creating the dataset from a series of construction timelapse videos. It is then possible to decide how many frames to extract from the videos and the number of classes to use for image classification. The aim is to create a support model for both construction companies and clients, allowing for insights into construction timelines, delays, and providing assistance for more accurate work planning.

## Installation and Setup
Instructions on setting up the project environment:
1. Clone the repository: 

 &nbsp;&nbsp;&nbsp;&nbsp;SSH: `git clone git@gitlab.com:i-fusilli1/ai_course_template.git` 

 &nbsp;&nbsp;&nbsp;&nbsp;HTTPS: `https://gitlab.com/i-fusilli1/ai_course_template.git`

2. Install dependencies: `pip install -r requirements.txt`

## Data
Data used in this project:
- **Raw Data**: You can find the raw data in the folder /data/raw/, where timelapse videos are present from which to extract the frames.
- **Processed Data**: In the processed data folder data/class*, you can find a set of folders representing different classifications. Each folder contains video frames in .png format corresponding to the construction percentage range indicated by the folder's name.

## Usage
How to run the project:
1. Download the repository in question.
2. To create the dataset, run the "main.py" file in the src/scripts directory (make sure to replace the paths in the code for creating the temporary folder where the frames for the "manual" dataset will be generated).
3. Once the graphical interface is open, select the folder from which to take the videos, the folder in which to place the subsequently extracted frames, the number of frames to extract from each video, and the number of classes to divide the dataset into. Finally, select whether to perform an automatic or manual execution (choose the frames one by one).
4. Once finished, you can start the models, always being careful to put the correct path of the folder where the dataset composed previously is located. The files to run are in the src/notebooks directory and have the .ipyb extension.
5. As a final step in the execution of these files, folders related to the newly trained models will be created to save the network states.
6. To test the models, there is a template at the path tests/main.ipynb. To use it, be careful to define the array of classes "class_names", insert the correct paths for image extraction, and call the model to use by the correct name.

The .py files and notebooks can be run through the graphical interface of the editor being used.

## Structure
- `/data`: Contains raw and processed data.
- `/src`: Source code for the project.
  - `/scripts`: Individual scripts or modules.
  - `/notebooks`: Jupyter notebooks or similar.
- `/tests`: Test cases for your application.
- `/docs`: Additional documentation in text format (e.g., LaTeX or Word).
- `/public`: Folder where GitLab pages will write static website. 
- `index.html`: Documentation in rich format (e.g., HTML, Markdown, JavaScript), will populate `public`.

## Contribution
If you want to contribute, you can work comfortably on a branch parallel to the main one. We will reserve the right to review the changes and potentially merge them into the main branch.

## Contact
Students who have participated in the project:
1. emanuele.corsi3@studio.unibo.it
2. mirco.chiarini@studio.unibo.it
3. antonio.sisinni@studio.unibo.it
