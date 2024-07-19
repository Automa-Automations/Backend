from typing import List, Union
import cv2
import numpy as np
import face_recognition
import logging
import math
from moviepy.editor import CompositeVideoClip, VideoClip
from errors import ClassTypeError, EditVideoError, ImpossibleError
from models import FaceFramePosition, ReturnMessage
from aliases import FacePositions, MoviePyClip

logger = logging.getLogger(__name__)


class FaceTrackingVideo:
    """
    Class to track a face in a video, along with cropping the video to a mobile short aspect ratio.
    """

    def __init__(self) -> None:
        self.frame_correction_number = (
            60  # meaning after each x frames, it will detect if there is a face
        )
        self.frame_index = 0
        self.all_frame_results: List[
            Union[FaceFramePosition, None]
        ]  # variable to keep all the frame indices data together

    def detect_faces(self, frame: np.ndarray) -> Union[tuple, None]:
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
        try:
            """
            Function to process each frame of the video
            Parameters:
            - frame: np.ndarray: The frame to process
            """
            current_indice = math.floor(self.frame_index / self.frame_correction_number)
            next_indice = current_indice + 1

            current_indice_dict = self.all_frame_results[current_indice]
            if next_indice > len(self.all_frame_results) - 1:
                next_indice_dict = current_indice_dict
            else:
                next_indice_dict = self.all_frame_results[next_indice]

            cx = 0.00
            cy = 0.00
            # When the first indice do not have a face
            if not current_indice_dict and current_indice == 0:
                # center both the cx and cy to be the center of the screen
                cx = frame.shape[1] / 2
                cy = frame.shape[0] / 2
            elif not current_indice_dict and current_indice > 0:
                # meaning that it is in the body and the current_frame_indice doesn't have a face.
                # look for the last face detected, and use that position
                current_index = current_indice - 1
                while current_index >= 0:
                    last_face_dict = self.all_frame_results[current_index]
                    if last_face_dict:
                        cx = last_face_dict.face_pos_x
                        cy = last_face_dict.face_pos_y
                        break
                    else:
                        cx = frame.shape[1] / 2
                        cy = frame.shape[0] / 2
                    current_index -= 1
            elif current_indice_dict and not next_indice_dict:
                cx = current_indice_dict.face_pos_x
                cy = current_indice_dict.face_pos_y
            else:
                # meaning that the current frame has a face detected and it isn't the first frame.
                if not current_indice_dict:
                    raise ImpossibleError(
                        message="Somehow 'current_indice_dict' is None",
                        explanation="This should not be possible, as if 'current_indice_dict' was None, it would have went down a different elif statement.",
                    )

                if not next_indice_dict:
                    raise ImpossibleError(
                        message="Somehow 'next_indice_dict' is None",
                        explanation="This should not be possible, as if 'next_indice_dict' was None, it would have went down a different elif statement.",
                    )

                cx, cy = self.calculate_face_pos(current_indice_dict, next_indice_dict)

            if not cx:
                raise EditVideoError(
                    message=f"Face Center Position X is not valid. CX: {cx}",
                    video_type="short",
                    action_type="process frame",
                )
            if not cy:
                raise EditVideoError(
                    message=f"Face Center Position Y is not valid. CX: {cy}",
                    video_type="short",
                    action_type="process frame",
                )

            # Define the target aspect ratio for cropping
            target_aspect_ratio = 9 / 16

            # Calculate the new width based on the target aspect ratio
            new_width = int(frame.shape[0] * target_aspect_ratio)

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
                x_start = int(
                    frame.shape[1] - new_width
                )  # start the x_start new_width from the right
                x_end = int(frame.shape[1])  # put x_end at the end of the frame

            # Crop the frame
            cropped_frame = frame[y_start:y_end, x_start:x_end]

            # Resize the cropped frame to the desired size (maintaining original height)
            resized_frame = cv2.resize(
                cropped_frame,
                (int(frame.shape[0] * target_aspect_ratio), frame.shape[0]),
            )

            self.frame_index += 1

            return resized_frame
        except Exception as e:
            raise EditVideoError(
                message=f"An error occurred while processing the frame: {e}",
                video_type="short",
                action_type="process frame",
            ) from e

    def calculate_face_pos(
        self,
        current_indice_dict: FaceFramePosition,
        next_indice_dict: FaceFramePosition,
    ) -> tuple[float, float]:
        """
        Function to calculate the current frame face positions
        Parameters:
        - current_indice_dict: FaceFramePositionDict: The dictionary of the face position for the current frame
        - next_indice_dict: FaceFramePositionDict: The dictionary of the face position for the next frame
        - frame_index: int: The index of the frame in the video
        Returns tuple[cx, cy] - a tuple with the center face position of x and y
        """
        current_indice_index = current_indice_dict.frame_index
        next_indice_index = next_indice_dict.frame_index

        x_difference = next_indice_dict.face_pos_x - current_indice_dict.face_pos_x
        y_difference = next_indice_dict.face_pos_y - current_indice_dict.face_pos_y
        frame_difference = next_indice_index - current_indice_index

        # do this so that it doesn't divide by zero, when the last frame in the video is a frame where we checked if there was a face detected
        if frame_difference == 0:
            frame_difference = 1

        frame_increment_x = x_difference / frame_difference
        frame_increment_y = y_difference / frame_difference
        curr_frame_after_curr_index = self.frame_index - current_indice_index

        cx = (
            current_indice_dict.face_pos_x
            + curr_frame_after_curr_index * frame_increment_x
        )
        cy = (
            current_indice_dict.face_pos_y
            + curr_frame_after_curr_index * frame_increment_y
        )
        return cx, cy

    def collect_face_position(
        self, frame: np.ndarray, indice_index: int
    ) -> FacePositions:
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

            return FaceFramePosition(
                frame_index=indice_index,
                face_pos_x=center_x,
                face_pos_y=center_y,
            )
        else:
            logger.info("No face detected in the frame")
            return ReturnMessage(message="No face detected", status=None)

    def process_short(self, video_clip: MoviePyClip) -> MoviePyClip:
        """
        Method called to process a short to have face detection, along with the right aspect ratio.
        Parameters:
        - video_clip: MoviePyClip: The video clip
        Returns MoviePyClip - the processed video clip
        """

        try:
            logger.info("Collecting face positions...")

            video_fps = video_clip.fps
            if not video_fps:
                raise ValueError("The video clip must have a valid FPS value")

            nframes = int(video_clip.duration * video_clip.fps)

            all_frame_results: List[Union[FaceFramePosition, None]] = []
            for fidx in range(0, nframes, self.frame_correction_number):
                frame: np.ndarray = video_clip.get_frame(fidx / video_fps)
                frame_result = self.collect_face_position(frame, fidx)
                # see if frame type is FramePositionDict
                if isinstance(frame_result, FaceFramePosition):
                    # since we know it is the correct type, since frame_index is a key in FaceFramePositionDict. Just doing this to remove type warnings
                    all_frame_results.append(frame_result)
                else:
                    self.__handle_face_frame_empty(frame_result)
                    all_frame_results.append(None)

            # Add a final position:
            final_frame_dict = self.collect_face_position(
                video_clip.get_frame(nframes / video_fps), nframes
            )
            if isinstance(final_frame_dict, FaceFramePosition):
                all_frame_results.append(final_frame_dict)
            else:
                self.__handle_face_frame_empty(final_frame_dict)
                all_frame_results.append(all_frame_results[-1])

            self.all_frame_results = all_frame_results
            self.frame_index = 1

            processed_clip = video_clip.fl_image(self.process_frame)
            type_checker = (CompositeVideoClip, VideoClip)
            processed_clip_type = type(processed_clip)
            if not isinstance(processed_clip_type, type_checker):
                raise ClassTypeError(
                    message=f"Processed Short Clip is not a valid type.",
                    types=type_checker,
                    got_class_type=processed_clip_type,
                )
            else:
                processed_clip: MoviePyClip = processed_clip
                return processed_clip
        except Exception as e:
            raise EditVideoError(
                message=f"Errror processing short: {e}",
                video_type="short",
                action_type="process short",
            ) from e

    def __handle_face_frame_empty(self, frame_dict: FacePositions):
        if not frame_dict:
            logger.warning(
                "Received an empty frame. This isn't suppose to happen. Appending None"
            )
