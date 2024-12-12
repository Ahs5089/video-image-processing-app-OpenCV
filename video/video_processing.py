import cv2
import numpy as np
from tkinter import Tk, filedialog, messagebox, ttk
import tkinter as tk

# Globals
object_paths = {}
selected_effect = "Blur"
count_objects_enabled = False
visualize_paths_enabled = False
video_writer = None
trackers = []  # This is where trackers will be stored


def select_video():
    """Prompt user to select a video file."""
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    return file_path


def save_video():
    """Prompt user to select a location and name for saving the video."""
    file_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi"), ("MP4 files", "*.mp4")])
    return file_path


def resize_frame_to_fit_screen(frame, max_width, max_height):
    """Resize the frame to fit within the given screen dimensions."""
    height, width = frame.shape[:2]
    scaling_factor = min(max_width / width, max_height / height)
    if scaling_factor < 1.0:
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor) 
        frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return frame


def pixelate_roi(roi, block_size=10):
    """Apply pixelation effect to ROI."""
    h, w = roi.shape[:2]
    roi = cv2.resize(roi, (w // block_size, h // block_size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_NEAREST)
    return roi


def apply_sepia(roi):
    """Apply sepia effect to ROI."""
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia_roi = cv2.transform(roi, kernel)
    return np.clip(sepia_roi, 0, 255).astype(np.uint8)


def update_paths(object_id, bbox):
    """Update the path for a tracked object."""
    global object_paths
    x, y, w, h = [int(i) for i in bbox]
    center = (x + w // 2, y + h // 2)
    if object_id not in object_paths:
        object_paths[object_id] = []  # Initialize path for the object
    object_paths[object_id].append(center)  # Add the new center to the path
    if len(object_paths[object_id]) > 50:  # Adjust path length as needed
        object_paths[object_id].pop(0)


def draw_paths(frame):
    """Draw the paths of tracked objects on the frame."""
    global object_paths
    for object_id, path in object_paths.items():
        for i in range(1, len(path)):
            if path[i - 1] is None or path[i] is None:
                continue
            cv2.line(frame, path[i - 1], path[i], (0, 255, 0), 2)


def process_video(video_path, screen_width, screen_height):
    global selected_effect, count_objects_enabled, visualize_paths_enabled, video_writer, trackers

    if not video_path:
        tk.messagebox.showwarning("No Video Selected", "Please select a video file.")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        tk.messagebox.showerror("Error", "Unable to open the video file.")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_file = save_video()
    if not output_file:
        tk.messagebox.showwarning("No File Name", "No file name provided for saving the video.")
        return

    video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'MJPG'), fps, (frame_width, frame_height))

    
    ret, frame = cap.read()
    if not ret:
        tk.messagebox.showerror("Error", "Unable to read the video file.")
        return
    # Ensure the frame matches the dimensions of the video writer
    if frame.shape[1] != frame_width or frame.shape[1] != frame_height:
        frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
        



    tk.messagebox.showinfo("Instructions", "Select initial objects to track. Press ENTER after each selection and ESC when done.")
    rois = []
    while True:
        roi = cv2.selectROI("Select Objects to Track (Press ESC when done)", frame, fromCenter=False, showCrosshair=True)
        if sum(roi) == 0:
            break
        rois.append(roi)
    cv2.destroyAllWindows()

    if not rois:
        tk.messagebox.showerror("Error", "No objects selected to track.")
        return
    

    trackers = [cv2.TrackerCSRT_create() for _ in rois]
    for tracker, roi in zip(trackers, rois):
        tracker.init(frame, tuple(roi))

    paused = False

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break
            
            
            # Ensure the frame matches the dimensions of the video writer
            if frame.shape[1] != frame_width or frame.shape[0] != frame_height:
                frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
                

        for tracker in trackers:
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = [int(i) for i in bbox]
                roi = frame[y:y + h, x:x + w]

                # Check if the ROI is not empty
                if roi.size == 0:
                    continue  # Skip if the ROI is empty

                if selected_effect == "Blur":
                    roi = cv2.GaussianBlur(roi, (25, 25), 30)
                elif selected_effect == "Pixelate":
                    roi = pixelate_roi(roi)
                elif selected_effect == "Sepia":
                    roi = apply_sepia(roi)

                frame[y:y + h, x:x + w] = roi

        if count_objects_enabled:
            cv2.putText(frame, f"Objects Tracked: {len(trackers)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if visualize_paths_enabled:
            draw_paths(frame)

        # Write the frame to the video writer
        video_writer.write(frame)

        cv2.imshow("Video Processing", frame)
        key = cv2.waitKey(1) & 0xFF

        # Key event handling
        if key == ord('q'):  # Quit
            break
        elif key == ord('p'):  # Pause/Resume
            paused = not paused
        elif key == ord('a') and paused:  # Add more ROIs while paused
            tk.messagebox.showinfo("Add Tracks", "Select additional objects to track. Press ENTER after each selection and ESC when done.")
            while True:
                roi = cv2.selectROI("Add Objects to Track (Press ESC when done)", frame, fromCenter=False, showCrosshair=True)
                if sum(roi) == 0:
                    break
                tracker = cv2.TrackerCSRT_create()
                tracker.init(frame, tuple(roi))  # Initialize the tracker with the current paused frame
                trackers.append(tracker)  # Append the new tracker
            cv2.destroyAllWindows()  # Close ROI window

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
    tk.messagebox.showinfo("Video Saved", f"Processed video saved as {output_file}")

def start_processing(algorithm, effect, count_objects, visualize_paths):
    global selected_effect, count_objects_enabled, visualize_paths_enabled
    selected_effect = effect
    count_objects_enabled = count_objects
    visualize_paths_enabled = visualize_paths

    video_path = select_video()
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    process_video(video_path, screen_width, screen_height)


def create_gui():
    root = Tk()
    root.title("Video Processing")
    root.geometry("400x300")

    ttk.Label(root, text="Select Tracking Algorithm:").pack()
    algo_choice = ttk.Combobox(root, values=["CSRT", "KCF", "MIL"], state="readonly")
    algo_choice.set("CSRT")
    algo_choice.pack()

    ttk.Label(root, text="Select Effect:").pack()
    effect_choice = ttk.Combobox(root, values=["Blur", "Pixelate", "Sepia"], state="readonly")
    effect_choice.set("Blur")
    effect_choice.pack()

    count_objects_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Count Objects", variable=count_objects_var).pack()

    visualize_path_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Visualize Paths", variable=visualize_path_var).pack()

    ttk.Button(root, text="Start", command=lambda: start_processing(algo_choice.get(), effect_choice.get(), count_objects_var.get(), visualize_path_var.get())).pack()

    root.mainloop()


if __name__ == "__main__":
    create_gui()
