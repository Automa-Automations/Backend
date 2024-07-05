from typing import Any, Optional, Callable, List, Union
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

    def process_frame(self, frame: np.ndarray) -> Union[np.ndarray, None]:
        """
        Function to process each frame of the video
        Parameters:
        - frame: np.ndarray: The frame to process
        """
        current_indice = math.floor(self.frame_index / 90)
        next_indice = math.ceil(self.frame_index / 90)

        #
        # if self.frame_index % self.frame_correction_number == 0:
        #     # we are on a frame where face was checked
        #     logger.info(f"Processing frame {self.frame_index}...")
        #

        current_indice_dict = self.all_frame_results[current_indice]
        next_indice_dict = self.all_frame_results[next_indice]

        cx = 0
        cy = 0
        # When the first indice do not have a face
        if not current_indice_dict and current_indice == 0:
            # center both the cx and cy to be the center of the screen
            cx = frame.shape[1] / 2
            cy = frame.shape[0] / 2
        elif not current_indice_dict and current_indice > 0:
            # meaning that it is in the body and the current_frame_indice doesn't have a face.
            # look for the last face detected, and use that position
            current_index = current_indice - 1
            while current_index > 0:
                last_face_dict = self.all_frame_results[current_index]
                if last_face_dict:
                    cx = last_face_dict["face_pos_x"]
                    cy = last_face_dict["face_pos_y"]
                    break
                else:
                    cx = frame.shape[1] / 2
                    cy = frame.shape[0] / 2
                current_index -= 1
        elif current_indice_dict and not next_indice_dict:
            cx = current_indice_dict["face_pos_x"]
            cy = current_indice_dict["face_pos_y"]
        else:
            # meaning that the current frame has a face detected and it isn't the first frame.
            current_indice_dict_correct_type: FaceFramePositionDict = json.loads(
                json.dumps(current_indice_dict)
            )
            next_indice_dict_correct_type: FaceFramePositionDict = json.loads(
                json.dumps(next_indice_dict)
            )
            cx, cy = self.calculate_face_pos(
                current_indice_dict_correct_type, next_indice_dict_correct_type
            )

        if not cx:
            logger.error("The face position is not defined, cx is undefined")
            return
        if not cy:
            logger.error("The face position is not defined, cy is undefined")
            return

        # Calculate the aspect ratio of the original frame
        original_aspect_ratio = frame.shape[1] / frame.shape[0]

        # Define the target aspect ratio for cropping
        target_aspect_ratio = 9 / 16

        # Calculate the new width based on the target aspect ratio
        new_width = frame.shape[0] * target_aspect_ratio

        # Center crop the frame
        x_start = int(cx - new_width / 2)
        x_end = int(cx + new_width / 2)

        # keep the y the same, as it will always be full width and height
        y_start = 0
        y_end = frame.shape[0]

        # Ensure the cropping region is within bounds
        x_start = max(0, x_start)  # make sure x_start is not less than 0
        x_end = min(
            frame.shape[1], x_end
        )  # make sure that x_end is not greater than the width of the frame
        if (
            x_end - x_start < new_width
        ):  # meaning if the frame has overlapped, the crop region is too small. It hase overlapped at the right side of the frame.
            x_start = (
                frame.shape[1] - new_width
            )  # start the x_start new_width from the right
            x_end = frame.shape[1]  # put x_end at the end of the frame

        # Crop the frame
        cropped_frame = frame[y_start:y_end, x_start:x_end]

        # Resize the cropped frame to the desired size (maintaining original height)
        resized_frame = cv2.resize(
            cropped_frame,
            (int(frame.shape[0] * target_aspect_ratio), frame.shape[0]),
        )

        self.frame_index += 1

        return resized_frame

    def calculate_face_pos(
        self,
        current_indice_dict: FaceFramePositionDict,
        next_indice_dict: FaceFramePositionDict,
    ) -> tuple[float, float]:
        """
        Function to calculate the current frame face positions
        Parameters:
        - current_indice_dict: FaceFramePositionDict: The dictionary of the face position for the current frame
        - next_indice_dict: FaceFramePositionDict: The dictionary of the face position for the next frame
        - frame_index: int: The index of the frame in the video
        Returns tuple[cx, cy] - a tuple with the center face position of x and y
        """
        current_indice_index = current_indice_dict["frame_index"]
        next_indice_index = next_indice_dict["frame_index"]

        x_difference = (
            next_indice_dict["face_pos_x"] - current_indice_dict["face_pos_x"]
        )
        y_difference = (
            next_indice_dict["face_pos_y"] - current_indice_dict["face_pos_y"]
        )
        frame_difference = next_indice_index - current_indice_index

        frame_increment_x = x_difference / frame_difference
        frame_increment_y = y_difference / frame_difference
        curr_frame_after_curr_index = self.frame_index - current_indice_index

        cx: float = (
            current_indice_dict["face_pos_x"]
            + curr_frame_after_curr_index * frame_increment_x
        )
        cy: float = (
            current_indice_dict["face_pos_y"]
            + curr_frame_after_curr_index * frame_increment_y
        )
        return cx, cy

    def collect_face_position(
        self, frame: np.ndarray, indice_index: int
    ) -> Optional[Union[FaceFramePositionDict, MessageReturnDict]]:
        """
        Collect the face position for a given frame
        Parameters:
        - frame: np.ndarray: The frame to collect the face position for
        - indice_index: str: The index of the frame in the video
        Returns FaceFramePositionDict - a dictionary with the face position if a face is detected, otherwise None
        """
        if not len(frame):
            logger.warning("Received an empty frame.")
            return None

        face_coordinates = self.detect_faces(frame)

        if face_coordinates:
            left, top, right, bottom = face_coordinates
            center_x, center_y = (left + right) / 2.0, (top + bottom) / 2.0

            return {
                "frame_index": indice_index,
                "face_pos_x": center_x,
                "face_pos_y": center_y,
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
            frame_result = self.collect_face_position(frame, fidx)
            if frame_result:
                # see if frame type is FramePositionDict
                if "frame_index" in frame_result:
                    # since we know it is the correct type, since frame_index is a key in FaceFramePositionDict. Just doing this to remove type warnings
                    correct_type_frame_result: FaceFramePositionDict = json.loads(
                        json.dumps(frame_result)
                    )
                    all_frame_results.append(correct_type_frame_result)
                else:
                    # meaning the frame didn't detect a face
                    all_frame_results.append(None)
            else:
                logger.warning("The frame result is None")

        # Add a final position:
        final_frame_dict = self.collect_face_position(
            video_clip.get_frame(nframes / video_fps), nframes
        )
        if final_frame_dict and "frame_index" in final_frame_dict:
            final_frame: FaceFramePositionDict = json.loads(
                json.dumps(final_frame_dict)
            )
            all_frame_results.append(final_frame)
        else:
            all_frame_results.append(all_frame_results[-1])

        self.all_frame_results = all_frame_results

        # Process each frame of the video:
        self.frame_index = 1

        # Create an interpolation function
        processed_clip = video_clip.fl_image(self.process_frame)

        return processed_clip
