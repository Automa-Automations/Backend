from dataclasses import dataclass
from typing import Any, Optional, Callable, List
import cv2
import numpy as np
import face_recognition
from scipy.interpolate import interp1d

@dataclass
class FaceTrackingVideo:
    frame_index: int = 0
    face_cx: Optional[float] = None
    face_cy: Optional[float] = None
    target_face_cx: Optional[float] = None
    target_face_cy: Optional[float] = None
    face_window_len: Optional[int] = None
    face_detector: Optional[Any] = None
    detect_face_func: Optional[Callable] = None
    frame_indices: Optional[List[int]] = None
    face_pos_x: Optional[List[float]] = None
    face_pos_y: Optional[List[float]] = None
    face_sizes: Optional[List[float]] = None
    interp_fcx_func: Optional[Callable] = None
    interp_fcy_func: Optional[Callable] = None
    interp_fsize_func: Optional[Callable] = None
    current_fsize: Optional[float] = None

    def detect_faces(self, frame):
        """Helper method to detect a face"""
        if self.face_detector is None:
            print("Initializing face_recognition detector...")
            self.face_detector = face_recognition

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = self.face_detector.face_locations(rgb_frame, model="hog")

        if face_locations:
            # Return only the first detected face
            top, right, bottom, left = face_locations[0]
            return (left, top, right, bottom)
        else:
            return None

    def process_frame(self, frame):
        """Function to process each frame of the video"""
        if self.frame_index % self.face_window_len == 0:
            print(f"Processing frame {self.frame_index}")

        # Perform interpolation to get the face x/y position:
        cx = self.interp_fcx_func(self.frame_index)
        cy = self.interp_fcy_func(self.frame_index)
        fsize = self.interp_fsize_func(self.frame_index)

        # Calculate the aspect ratio of the original frame
        original_aspect_ratio = frame.shape[1] / frame.shape[0]

        # Define the target aspect ratio for cropping
        target_aspect_ratio = 9 / 16

        # Calculate the new width based on the target aspect ratio
        new_width = frame.shape[0] * target_aspect_ratio

        # Center crop the frame
        x_start = int(cx - new_width / 2)
        x_end = int(cx + new_width / 2)
        y_start = 0
        y_end = frame.shape[0]

        # Ensure the cropping region is within bounds
        x_start = max(0, x_start)
        x_end = min(frame.shape[1], x_end)
        if x_end - x_start < new_width:
            x_start = frame.shape[1] - new_width
            x_end = frame.shape[1]

        # Crop the frame
        cropped_frame = frame[y_start:y_end, x_start:x_end]

        # Resize the cropped frame to the desired size (maintaining original height)
        resized_frame = cv2.resize(cropped_frame, (int(frame.shape[0] * target_aspect_ratio), frame.shape[0]))

        self.frame_index += 1

        return resized_frame

    def collect_face_position(self, frame, nframes):
        """Collect the face position for a given frame"""
        if self.frame_index % self.face_window_len == 0:
            print(f"Collecting face at frame {self.frame_index}/{nframes}")
            face_coordinates = self.detect_faces(frame)

            if face_coordinates is not None:
                left, top, right, bottom = face_coordinates
                center_x, center_y = (left + right) / 2.0, (top + bottom) / 2.0
                size = max(abs(right - left), abs(top - bottom))

                self.frame_indices.append(self.frame_index)
                self.face_pos_x.append(center_x)
                self.face_pos_y.append(center_y)
                self.face_sizes.append(size)

        self.frame_index += 1

        return frame

    def process_short(self, video_clip):
        """Method called to process a short to have face detection, along with the right aspect ratio"""

        self.face_window_len = 90
        self.frame_index = 0

        # First we collect all the required center positions for a given frame index:
        self.frame_indices = []
        self.face_pos_x = []
        self.face_pos_y = []
        self.face_sizes = []

        print("Collecting face positions...")
        nframes = int(video_clip.duration * video_clip.fps)

        for fidx in range(0, nframes, self.face_window_len):
            self.frame_index = fidx
            frame = video_clip.get_frame(fidx / video_clip.fps)
            self.collect_face_position(frame, nframes)

        # Add a final position:
        self.frame_indices.append(nframes + 1)
        self.face_pos_x.append(self.face_pos_x[-1])
        self.face_pos_y.append(self.face_pos_y[-1])
        self.face_sizes.append(self.face_sizes[-1])

        self.current_fsize = self.face_sizes[0]

        print(f"Done collecting {len(self.frame_indices)} face positions")

        # Process each frame of the video:
        self.frame_index = 0

        # Create an interpolation function
        imode = "linear"

        self.interp_fcx_func = interp1d(np.array(self.frame_indices), np.array(self.face_pos_x), kind=imode)
        self.interp_fcy_func = interp1d(np.array(self.frame_indices), np.array(self.face_pos_y), kind=imode)
        self.interp_fsize_func = interp1d(np.array(self.frame_indices), np.array(self.face_sizes), kind=imode)

        processed_clip = video_clip.fl_image(self.process_frame)

        return processed_clip
