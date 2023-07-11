# What it does

After running the main.py file, if all libraries are installed, two windows will appear. One is the video feed of your camera, and the other window will appear black until an exam is detected in the feed.

Video feed           |  Exam window
:-------------------------:|:-------------------------:
![image](https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/f82cac3d-832f-447b-af80-1c1798a06e27)  |  <img src="https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/6c756d0b-05fa-46b5-9851-bd26bd67575c" width="75%" height="75%" />


Only exam sheets made by the "fer_pdf.py" file will be detected. That program outputs a png of an exam with a given number of questions, it then needs to be printed. The created file will look like this:

<img src="https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/0b2fa9a5-2dbf-41d0-bea3-6aedb1f98db2" width="30%" height="30%" />

And if an exam is detected in the video feed, it will be shown and resized in the exam window

Video feed           |  Exam window
:-------------------------:|:-------------------------:
![image](https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/dbbf7ce4-4e12-4ccd-beb5-a67e04d83433) | <img src="https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/45a1230e-05f1-4f2f-bdde-91f5a19e72b9" width="75%" height="75%" />

When an exam is detected, if the letter "e" is pressed, the marked answers will start to get detected, the frame will freeze and the marked answers will appear inside a green rectangle:

<img src="https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/55116b7f-7675-4c80-873a-c39b2df48aae" width="40%" height="40%" />

As you can see not all answers are marked correctly, for the detection to improve the following things need to be done:

- Account for the camera warp, straight lines might seem curved when the camera has a high FOV or the object is too close

- Train a better neural network to differentiate between marked and not marked answers.
