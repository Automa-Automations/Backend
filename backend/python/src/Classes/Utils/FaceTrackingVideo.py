from typing import Any, AnyStr, Optional, Callable, List, TypedDict, Union
import cv2
from moviepy.editor import CompositeVideoClip, VideoClip
import numpy as np
import face_recognition
from numpy._typing import _UnknownType
from scipy.interpolate import interp1d
import logging
import json
import math

from models import FaceFramePositionDict, MessageReturnDict

logger = logging.getLogger(__name__)


class FaceTrackingVideo:
    """
    Class to track a face in a video, along with cropping the video to a mobile short aspect ratio.
    """

    def __init__(self) -> None:
        self.frame_correction_number = (
            90  # meaning after each x frames, it will detect if there is a face
        )
        self.frame_index = 0
        self.frame_indices = []
        self.face_pos_x: List[float] = []
        self.face_pos_y: List[float] = []
        self.face_sizes: List[float] = []
        self.imode = "linear"
        self.all_frame_results: List[
            Union[FaceFramePositionDict, None]
        ]  # variable to keep all the frame indices data together
        self.face_cx: Optional[float] = None
        self.face_cy: Optional[float] = None
        self.target_face_cx: Optional[float] = None
        self.target_face_cy: Optional[float] = None
        self.detect_face_func: Optional[Callable] = None
        self.interp_fcx_func: Optional[Callable] = None
        self.interp_fcy_func: Optional[Callable] = None
        self.interp_fsize_func: Optional[Callable] = None

    def detect_faces(self, frame: np.ndarray) -> Optional[tuple]:
        """
        Helper method to detect a face.
        Parameters:
        - frame: np.ndarray: The frame to detect the face in
        """
        # Check the frame's data type and convert if necessary
        if frame.dtype != np.uint8:
            frame = frame.astype(np.uint8)

        # Ensure the frame is in RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame, model="hog")

        if face_locations:
            # Return only the first detected face
            top, right, bottom, left = face_locations[0]
            return (left, top, right, bottom)
        else:
            return None

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Function to process each frame of the video
        Parameters:
        - frame: np.ndarray: The frame to process
        """
        self.current_indice = math.floor(self.frame_index / 90)
        self.next_indice = math.ceil(self.frame_index / 90)

        #
        # if self.frame_index % self.frame_correction_number == 0:
        #     # we are on a frame where face was checked
        #     logger.info(f"Processing frame {self.frame_index}...")
        #

        current_indice_dict = self.all_frame_results[self.current_indice]
        next_indice_dict = self.all_frame_results[self.next_indice]

        # When the first indice do not have a face
        if not current_indice_dict and self.current_indice == 0:
            # center both the cx, cy, and fsize to be the center of the screen
            cx = frame.shape[1] / 2
            cy = frame.shape[0] / 2
            fsize = frame.shape[0] / 2
        # Perform interpolation to get the face x/y position:
        cx = self.__interp_fcx_func(self.frame_index)
        cy = self.__interp_fcy_func(self.frame_index)
        fsize = self.__interp_fsize_func(self.frame_index)

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
        resized_frame = cv2.resize(
            cropped_frame,
            (int(frame.shape[0] * target_aspect_ratio), frame.shape[0]),
        )

        self.frame_index += 1

        return resized_frame

    def collect_face_position(
        self, frame: np.ndarray
    ) -> Optional[Union[FaceFramePositionDict, MessageReturnDict]]:
        """
        Collect the face position for a given frame
        Parameters:
        - frame: np.ndarray: The frame to collect the face position for
        Returns FaceFramePositionDict - a dictionary with the face position if a face is detected, otherwise None
        """
        if not frame:
            logger.warning("Received an empty frame.")
            return None

        face_coordinates = self.detect_faces(frame)

        if face_coordinates:
            left, top, right, bottom = face_coordinates
            center_x, center_y = (left + right) / 2.0, (top + bottom) / 2.0
            size = max(abs(right - left), abs(top - bottom))

            return {
                "frame_index": self.frame_index,
                "face_pos_x": center_x,
                "face_pos_y": center_y,
                "face_size": size,
            }
        else:
            logger.info("No face detected in the frame")
            return {
                "message": "No face detected",
                "status": None,
            }

    def process_short(self, video_clip: Union[Any, VideoClip, CompositeVideoClip]):
        """Method called to process a short to have face detection, along with the right aspect ratio"""

        logger.info("Collecting face positions...")
        video_fps = video_clip.fps
        if not video_fps:
            raise ValueError("The video clip must have a valid FPS value")

        nframes = int(video_clip.duration * video_clip.fps)

        all_frame_results: List[Union[FaceFramePositionDict, None]] = []
        for fidx in range(0, nframes, self.frame_correction_number):
            frame: np.ndarray = video_clip.get_frame(fidx / video_fps)
            frame_result = self.collect_face_position(frame)
            if frame_result:
                # see if frame type is FramePositionDict
                if frame_result.get("frame_index"):
                    # since we know it is the correct type, since frame_index is a key in FaceFramePositionDict. Just doing this to remove type warnings
                    correct_type_frame_result: FaceFramePositionDict = json.loads(
                        json.dumps(frame_result)
                    )
                    all_frame_results.append(correct_type_frame_result)
                else:
                    # meaning the frame didn't detect a face
                    all_frame_results.append(None)

        # Add a final position:
        final_frame_dict = self.collect_face_position(video_clip.get_frame(nframes))
        if final_frame_dict and final_frame_dict.get("frame_index"):
            final_frame: FaceFramePositionDict = json.loads(
                json.dumps(final_frame_dict)
            )
            all_frame_results.append(final_frame)
        else:
            all_frame_results.append(all_frame_results[-1])

        self.current_fsize = self.face_sizes[0]
        self.all_frame_results = all_frame_results

        logger.info(f"Done collecting {len(self.frame_indices)} face positions")

        # Process each frame of the video:
        self.frame_index = 0

        # Create an interpolation function
        processed_clip = video_clip.fl_image(self.process_frame)

        return processed_clip

    def __interp_fcx_func(self, frame_index: int) -> _UnknownType:
        interpolator = interp1d(
            np.array(self.frame_indices),
            np.array(self.face_pos_x),
            kind=self.imode,
        )
        return interpolator(frame_index)

    def __interp_fcy_func(self, frame_index: int) -> _UnknownType:
        interpolator = interp1d(
            np.array(self.frame_indices),
            np.array(self.face_pos_y),
            kind=self.imode,
        )
        return interpolator(frame_index)

    def __interp_fsize_func(self, frame_index: int) -> _UnknownType:
        interpolator = interp1d(
            np.array(self.frame_indices),
            np.array(self.face_sizes),
            kind=self.imode,
        )
        return interpolator(frame_index)
