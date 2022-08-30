# Project Description
The goal of this project is to build an intelligent system that performs clustering on face  
images. Face clustering is used in mobile phones to categorize gallery images. Such a  
system can also be used to review CCTV videos. This system is implemented in the form of
a desktop software. The software has a graphical interface suitable for communication with
user and consists of several major parts. In the first part, the user identifies the folder
where there are a number of image. The program finds all pictures in this folder and presents
them to the user, then it processes the images and finds every face image in them. There are
plenty of algorithms that we can use for face detection e.g. MTCNN which is used in this project.
After detecting the face images, another algorithm is used to find a representation for each face.
This representation is later used in a clustering algorithm and images are categorized according to
the identity of the people in them. Finally images of different people are saved in separate
folders and the user can view them.

![home](https://github.com/mohammadmozafari/face-clustering/blob/master/1.png?raw=true)
