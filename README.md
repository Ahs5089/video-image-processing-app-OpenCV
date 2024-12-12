# Video and Image Processing Application

## Overview
This project consists of two Python applications for **video processing** and **image processing**. It allows users to apply various effects, track objects in videos, and process images with convolution filters. The GUI for both applications is built using `Tkinter`, and core functionalities leverage `OpenCV`.

## Features
### Video Processing
- **Object Tracking**: Tracks multiple objects in a video using algorithms like `CSRT`, `KCF`, and `MIL`.
- **Effects**: Applies effects such as Blur, Sepia, and Pixelation to selected objects in the video.
- **Path Visualization**: Displays the movement paths of tracked objects.
- **Object Counting**: Displays the count of tracked objects in real-time.
- **Video Saving**: Save the processed video with all applied effects.

### Image Processing
- **Effects**: Apply convolution effects such as Box Blur, Gaussian Blur, Edge Detection, and Sharpening.
- **Real-time Preview**: View processed images alongside the original.
- **Image Saving**: Save the processed image.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/video-image-processing.git
   cd video-image-processing
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Video Processing
1. Run the `video_processing.py` script:
   ```bash
   python video_processing.py
   ```
2. Use the GUI to:
   - Select a video file.
   - Choose tracking algorithms and effects.
   - Enable object counting and path visualization if needed.
   - Process and save the video.

### Image Processing
1. Run the `image_processing.py` script:
   ```bash
   python image_processing.py
   ```
2. Use the GUI to:
   - Open an image file.
   - Apply desired effects.
   - Save the processed image.

## Requirements
- Python 3.8+
- Libraries:
  - `opencv-python`
  - `numpy`
  - `Pillow`
  - `tkinter` (included with Python)

Install the required libraries using:
```bash
pip install opencv-python numpy Pillow
```

## Project Structure
```
video-image-processing/
├── video_processing.py   # Video processing application
├── image_processing.py   # Image processing application
├── README.md             # Documentation
└── requirements.txt      # Python dependencies
```

## Screenshots
Add screenshots of your application (GUI, processed video, or image results) to showcase its functionality.

## Future Enhancements
- Add support for more tracking algorithms.
- Enable batch processing of videos and images.
- Improve the UI design for better user experience.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork this repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Added new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements
- [OpenCV](https://opencv.org/): For providing powerful computer vision libraries.
- [Pillow](https://python-pillow.org/): For image handling and processing.

---

**Developed with ❤️ by [Muhammad Ahsan](https://github.com/ahs5089)**.

