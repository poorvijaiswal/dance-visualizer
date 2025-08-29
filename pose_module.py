"""
Dance Performance Visualizer - Pose Detection Module

This module handles MediaPipe pose detection and gesture recognition.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, List, Tuple, Optional

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Movement history for gesture detection
        self.keypoint_history = []
        self.max_history = 10
        
        # Screen dimensions (will be set from main)
        self.screen_width = 1280
        self.screen_height = 720
        
    def set_screen_dimensions(self, width: int, height: int):
        """Set screen dimensions for coordinate normalization"""
        self.screen_width = width
        self.screen_height = height
    
    def detect_pose(self, frame: np.ndarray) -> Dict:
        """Detect pose and return processed keypoints"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        pose_data = {
            'landmarks': None,
            'keypoints': {},
            'gestures': [],
            'movement_energy': 0.0
        }
        
        if results.pose_landmarks:
            # Extract and normalize keypoints
            keypoints = self._extract_keypoints(results.pose_landmarks)
            pose_data['landmarks'] = results.pose_landmarks
            pose_data['keypoints'] = keypoints
            
            # Detect gestures and movement
            pose_data['gestures'] = self._detect_gestures(keypoints)
            pose_data['movement_energy'] = self._calculate_movement_energy(keypoints)
            
            # Update history
            self._update_history(keypoints)
        
        return pose_data
    
    def _extract_keypoints(self, landmarks) -> Dict[str, Tuple[int, int]]:
        """Extract and normalize key body points"""
        keypoints = {}
        
        # Key landmarks mapping
        key_landmarks = {
            'nose': 0,
            'left_shoulder': 11,
            'right_shoulder': 12,
            'left_elbow': 13,
            'right_elbow': 14,
            'left_wrist': 15,
            'right_wrist': 16,
            'left_hip': 23,
            'right_hip': 24,
            'left_knee': 25,
            'right_knee': 26,
            'left_ankle': 27,
            'right_ankle': 28
        }
        
        for name, idx in key_landmarks.items():
            landmark = landmarks.landmark[idx]
            # Convert to screen coordinates
            x = int(landmark.x * self.screen_width)
            y = int(landmark.y * self.screen_height)
            keypoints[name] = (x, y)
        
        # Calculate derived points
        if 'left_hip' in keypoints and 'right_hip' in keypoints:
            hip_center = (
                (keypoints['left_hip'][0] + keypoints['right_hip'][0]) // 2,
                (keypoints['left_hip'][1] + keypoints['right_hip'][1]) // 2
            )
            keypoints['hip_center'] = hip_center
        
        return keypoints
    
    def _detect_gestures(self, keypoints: Dict[str, Tuple[int, int]]) -> List[str]:
        """Detect specific dance gestures"""
        gestures = []
        
        if not keypoints:
            return gestures
        
        # Hands above head
        if ('left_wrist' in keypoints and 'right_wrist' in keypoints and 
            'nose' in keypoints):
            left_hand_y = keypoints['left_wrist'][1]
            right_hand_y = keypoints['right_wrist'][1]
            head_y = keypoints['nose'][1]
            
            if left_hand_y < head_y - 50 and right_hand_y < head_y - 50:
                gestures.append('hands_up')
        
        # Wide arm spread
        if ('left_wrist' in keypoints and 'right_wrist' in keypoints and
            'left_shoulder' in keypoints and 'right_shoulder' in keypoints):
            arm_span = abs(keypoints['left_wrist'][0] - keypoints['right_wrist'][0])
            shoulder_span = abs(keypoints['left_shoulder'][0] - keypoints['right_shoulder'][0])
            
            if arm_span > shoulder_span * 1.5:
                gestures.append('arms_wide')
        
        # Jump detection (requires history)
        if len(self.keypoint_history) > 3:
            gestures.extend(self._detect_jump())
        
        return gestures
    
    def _detect_jump(self) -> List[str]:
        """Detect jumping motion from movement history"""
        if len(self.keypoint_history) < 4:
            return []
        
        # Check hip center vertical movement
        recent_hips = []
        for frame in self.keypoint_history[-4:]:
            if 'hip_center' in frame:
                recent_hips.append(frame['hip_center'][1])
        
        if len(recent_hips) < 4:
            return []
        
        # Detect sudden upward movement
        vertical_velocity = recent_hips[-1] - recent_hips[-3]
        if vertical_velocity < -30:  # Moving up (y decreases)
            return ['jump']
        
        return []
    
    def _calculate_movement_energy(self, keypoints: Dict[str, Tuple[int, int]]) -> float:
        """Calculate overall movement energy"""
        if len(self.keypoint_history) < 2:
            return 0.0
        
        if not self.keypoint_history[-1]:
            return 0.0
        
        energy = 0.0
        prev_keypoints = self.keypoint_history[-1]
        
        # Calculate movement for key points
        key_points = ['left_wrist', 'right_wrist', 'hip_center']
        
        for point in key_points:
            if point in keypoints and point in prev_keypoints:
                dx = keypoints[point][0] - prev_keypoints[point][0]
                dy = keypoints[point][1] - prev_keypoints[point][1]
                energy += np.sqrt(dx*dx + dy*dy)
        
        return min(energy / 10.0, 10.0)  # Normalize to 0-10 range
    
    def _update_history(self, keypoints: Dict[str, Tuple[int, int]]):
        """Update movement history for gesture detection"""
        self.keypoint_history.append(keypoints.copy())
        if len(self.keypoint_history) > self.max_history:
            self.keypoint_history.pop(0)
    
    def draw_pose(self, frame: np.ndarray, pose_data: Dict) -> np.ndarray:
        """Draw pose landmarks on frame"""
        if pose_data['landmarks']:
            self.mp_drawing.draw_landmarks(
                frame, 
                pose_data['landmarks'], 
                self.mp_pose.POSE_CONNECTIONS
            )
        return frame
