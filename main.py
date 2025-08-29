"""
Dance Performance Visualizer

Setup Instructions:
1. Create virtual environment: python -m venv venv
2. Activate it: venv\Scripts\activate (Windows) or source venv/bin/activate (Linux/Mac)
3. Install dependencies: pip install -r requirements.txt
4. Run: python main.py
"""

import cv2
import pygame
import sys
import numpy as np

# Check for required modules
try:
    from pose_module import PoseDetector
    from visuals import VisualEffects
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please make sure you have installed all dependencies:")
    print("pip install -r requirements.txt")
    sys.exit(1)

class DanceVisualizer:
    def __init__(self):
        # Check camera availability
        test_cap = cv2.VideoCapture(0)
        if not test_cap.isOpened():
            print("Error: Could not open camera. Please check if your camera is available.")
            test_cap.release()
            sys.exit(1)
        test_cap.release()
        
        # Initialize Pygame
        try:
            pygame.init()
        except pygame.error as e:
            print(f"Error initializing Pygame: {e}")
            sys.exit(1)
        
        # Screen dimensions
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.VIDEO_WIDTH = 320
        self.VIDEO_HEIGHT = 240
        
        # Create main display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Dance Performance Visualizer")
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Initialize pose detector
        self.pose_detector = PoseDetector()
        self.pose_detector.set_screen_dimensions(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Initialize visual effects
        self.visual_effects = VisualEffects(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Control flags
        self.show_video = True
        self.fullscreen = False
        self.running = True
        
        # Performance tracking
        self.clock = pygame.time.Clock()
        self.fps_target = 30
    
    def handle_events(self):
        """Handle keyboard and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_v:
                    self.show_video = not self.show_video
                elif event.key == pygame.K_f:
                    self.toggle_fullscreen()
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # Update screen dimensions
            self.SCREEN_WIDTH = self.screen.get_width()
            self.SCREEN_HEIGHT = self.screen.get_height()
        else:
            self.screen = pygame.display.set_mode((1280, 720))
            self.SCREEN_WIDTH = 1280
            self.SCREEN_HEIGHT = 720
        
        # Update visual effects with new dimensions
        self.visual_effects = VisualEffects(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.pose_detector.set_screen_dimensions(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
    
    def process_frame(self):
        """Capture and process a single frame"""
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Detect pose
        pose_data = self.pose_detector.detect_pose(frame)
        
        # Draw pose on frame for debugging
        if self.show_video:
            frame_with_pose = self.pose_detector.draw_pose(frame.copy(), pose_data)
        else:
            frame_with_pose = None
        
        return frame_with_pose, pose_data
    
    def draw_debug_info(self, pose_data):
        """Draw debug information on screen"""
        if not pose_data:
            return
        
        font = pygame.font.Font(None, 36)
        y_offset = 10
        
        # Movement energy
        energy = pose_data.get('movement_energy', 0)
        energy_text = font.render(f"Energy: {energy:.1f}", True, (255, 255, 255))
        self.screen.blit(energy_text, (10, y_offset))
        y_offset += 30
        
        # Active gestures
        gestures = pose_data.get('gestures', [])
        if gestures:
            gesture_text = font.render(f"Gestures: {', '.join(gestures)}", True, (255, 255, 0))
            self.screen.blit(gesture_text, (10, y_offset))
            y_offset += 30
        
        # Controls
        controls = [
            "Controls:",
            "V - Toggle video",
            "F - Fullscreen",
            "Q - Quit"
        ]
        
        small_font = pygame.font.Font(None, 24)
        for i, control in enumerate(controls):
            color = (200, 200, 200) if i == 0 else (150, 150, 150)
            control_text = small_font.render(control, True, color)
            self.screen.blit(control_text, (10, self.SCREEN_HEIGHT - 100 + i * 20))
    
    def draw_video_window(self, frame):
        """Draw small video window with pose overlay"""
        if frame is None or not self.show_video:
            return
        
        # Resize frame for small window
        small_frame = cv2.resize(frame, (self.VIDEO_WIDTH, self.VIDEO_HEIGHT))
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Convert to pygame surface
        frame_surface = pygame.surfarray.make_surface(rgb_frame.swapaxes(0, 1))
        
        # Position video window in top-right corner
        video_x = self.SCREEN_WIDTH - self.VIDEO_WIDTH - 10
        video_y = 10
        
        # Draw border
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (video_x - 2, video_y - 2, 
                         self.VIDEO_WIDTH + 4, self.VIDEO_HEIGHT + 4), 2)
        
        # Blit video
        self.screen.blit(frame_surface, (video_x, video_y))
    
    def run(self):
        """Main application loop"""
        print("Dance Visualizer Starting...")
        print("Controls:")
        print("  V - Toggle video window")
        print("  F - Toggle fullscreen")
        print("  Q - Quit")
        
        while self.running:
            # Handle events
            self.handle_events()
            
            # Process camera frame
            frame_with_pose, pose_data = self.process_frame()
            
            # Update visual effects
            if pose_data:
                self.visual_effects.update(pose_data)
            
            # Draw everything
            self.visual_effects.draw(self.screen)
            
            # Draw debug info
            self.draw_debug_info(pose_data)
            
            # Draw video window
            self.draw_video_window(frame_with_pose)
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            self.clock.tick(self.fps_target)
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("=== Dance Performance Visualizer ===")
    print("Make sure you have activated your virtual environment!")
    print("If you haven't set up the environment yet:")
    print("1. python -m venv venv")
    print("2. venv\\Scripts\\activate  (Windows)")
    print("3. pip install -r requirements.txt")
    print("\nStarting visualizer...")
    
    try:
        visualizer = DanceVisualizer()
        visualizer.run()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
