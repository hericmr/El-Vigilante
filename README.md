# El Vigilante - Santos - Héric Moura's Final Project
#### Video Demo:  https://youtu.be/-QPwhqUjOpc
#### Description:

"El Vigilante - Santos" is a aplication that allows users to view real-time camera feeds from  some locations in Santos, Brazil. Developed in Python using OpenCV, this app leverages the public cameras from the Santos city government for a virtual watch.

The project is composed of a single Python script, `project.py`, which handles all the functionality of the program. The script starts by presenting the user  a list of available cameras to choose from. Each camera is associated with a unique number, and the user simply needs to input the number corresponding to the camera they wish to view. If any invalid inputs are inserted by the user a ValueError will be called.

Once a camera is selected, the program uses the OpenCV library to access the video stream from the camera and display it in a new window. The video stream continues indefinitely until the user decides to stop it by pressing the 'q' key.

`Ufortunaly in the codespace enviroment the OpenCV window does not open, this aplication needs to be instaled in a native graphic machine).`

This project uses the following Python libraries:
- OpenCV: For accessing and displaying the video streams.
- multiprocessing: For displaying diferent windows in same time.

##### Files:
- `project.py`: The main Python file that contains the functions for this project. This includes functions for displaying the menu, selecting the camera, and streaming the video feed.

- `requirements.txt`: A file listing all the Python libraries that the project depends on.

##### Functions:
- `show_menu()`: This function displays a text-based menu of the available camera locations to the user.

- `show_feed_camera(lugar, url)`: This function takes the location and URL of the camera as parameters. It establishes a connection with the camera feed and streams it onto an OpenCV window in real-time.

- `select_camera()`: This function lets the user select the camera location. It calls the `exibir_menu()` function to allow the user to choose the location, and then fetches the appropriate URL from the `cameras` dictionary.

- `main()`: The main function initializes the `cameras` dictionary with all the available camera locations and their respective URLs. It then calls the `select_camera()` function to start the program.

The app has been designed keeping simplicity and usability. Whether you're a local trying to monitor or a tourist looking to explore Santos virtually. I chose to develop this project because i wanted to show up my beautiful city, and to gain experience working with video streams and the OpenCV library.

 Very nice, dont you think?
