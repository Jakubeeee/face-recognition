# face-recognition
Simple application that features face detection and recognition. Also, it allows to apply various distortions on images before comparing.

---

Features:

- Simple graphical user interface
- The ability to use host device's camera
- Saving users and images of their faces in database
- Comparing two images containing faces
- Applying distortions to images before comparison

---

Used technologies:

- kivy for GUI
- dlib and face_recognition libraries for face comparison
- PIL and imgaug libraries for image manipulation
- numpy library
- sqlite embedded database
- git

---

In order to launch this application locally, you need to have a few things installed first.
- Visual Studio 2015 (first step from this page: https://www.learnopencv.com/install-opencv3-on-windows)
- Cmake (second step from this page: https://www.learnopencv.com/install-opencv3-on-windows)
- Dlib (steps 4, 5 and 6 from this page: https://www.learnopencv.com/install-dlib-on-windows)

---

config.py file allows you to change the application behaviour.
To apply some distortion to an image, you need to set the appropriate factor at desired level.
You can also change face comparison tolerance level, enable face encoding caching and more.
