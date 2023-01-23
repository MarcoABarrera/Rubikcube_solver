# Rubikcube_solver

The Rubik’s cube when placed in front of the webcam is captured and cropped.

Uses unsupervised learning(K-means clustering algorithm) to find the colors

The average hue, saturation and value of each tile are found and converted to the corresponding colour by matching the values with predefined data.

The colours are stored in a 3D array and processed to a format required by the kociemba algorithm which returns a solution sequence which is further processed to use only 5 stepper motors

The solution string is passed to an Arduino via serial port using pyserial which rotates the corresponding stepper motors
