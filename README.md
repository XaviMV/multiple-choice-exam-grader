# How to use it

This program automatically grades multiple-choice tests that have been done using the following template:

<p align="center">
  <img width="400" height="566" src="https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/0065c948-140f-4d08-8a01-771879749359">
</p>

What is needed in order to correct the exam is: the cheat sheet of the correct answers (also in the same template), and the exam that needs to be graded.

After running the GUI.py file this window will open, it displays the video of a detected camera in the computer:

![image](https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/78f214bb-bd1a-44bc-b6fc-b60da29df9ad)

When the answer sheet is shown in the feed, the "Select answer" button can be pressed. This will detect where all the correct answers are, it will also mark them in order to verify that they have been detected correctly.

![image](https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/a6bc4db0-0721-4617-93d0-0218dc2bc511)

After this is done, exams can be shown in front of the camera and corrected with the "Grade exam" button. At the bottom left of the window the number of correct, incorrect and not answered questions will be shown.

![image](https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/926edfcd-de53-40b5-ba49-838132a9d12f)

In order to correct more exams just click the "Next exam" button and repeat the last step for every new exam.

# Improvements

This project can be improved in many ways.

As of now the detection of correct and incorrect answers is only 99.5% accurate, in order to increase the accuracy the following things could be done:

- Increase the training samples (A total of 3600 samples were used in order to train the neural network that differentiates between marked and not marked answers)

- Reduce video distortion. Due to the high FOV of the camera straight lines in real life might appear curved in the display, this increases the distance between the calculated positions of the answers and the actual position. This can be clearly seen as the answers are not in the middle of the green or red boxes that surround them:

Centered answer:
![image](https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/e3a71225-9bf1-4c30-a5bb-a6fdcc1c00db)

Not so centered answer:
![image](https://github.com/XaviMV/multiple-choice-exam-grader/assets/70759474/bbdd3919-f0f2-42ff-ba32-b76134eb5ddd)

The interface could also be improved

More templates could be added: more than 3 possible answers per question and not only a 60 question template
