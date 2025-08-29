"""
Dance Performance Visualizer - Visual Effects Module

This module handles all the generative visual effects including:
- Particle systems
- Hand trails
- Gesture-based animations
- Dynamic backgrounds
- Energy-responsive color schemes

Author: Dance Visualizer Project
License: MIT
"""

import pygame
import numpy as np
import random
import math
from typing import List, Tuple, Dict

class Particle:
    def __init__(self, x: float, y: float, vx: float = 0, vy: float = 0, 
                 color: Tuple[int, int, int] = (255, 255, 255), 
                 life: float = 1.0, size: float = 3.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = 0.1
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 0.02
        
        # Fade color based on life
        alpha = self.life / self.max_life
        self.color = tuple(int(c * alpha) for c in self.color)
    
    def is_dead(self):
        return self.life <= 0
    
    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, 
                             (int(self.x), int(self.y)), int(self.size))

class VisualEffects:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.particles = []
        self.trails = []
        self.background_intensity = 0
        
        # Color palettes for different energy levels
        self.calm_colors = [(100, 150, 255), (150, 200, 255), (200, 220, 255)]
        self.energetic_colors = [(255, 100, 100), (255, 150, 50), (255, 200, 0)]
        self.neutral_colors = [(150, 150, 150), (200, 200, 200), (255, 255, 255)]
    
    def update(self, pose_data: Dict):
        """Update visual effects based on pose data"""
        keypoints = pose_data.get('keypoints', {})
        gestures = pose_data.get('gestures', [])
        energy = pose_data.get('movement_energy', 0)
        
        # Update background intensity based on movement
        self.background_intensity = min(energy * 20, 255)
        
        # Handle gestures
        self._handle_gestures(keypoints, gestures, energy)
        
        # Create ambient particles based on movement
        self._create_ambient_particles(keypoints, energy)
        
        # Update existing particles
        self._update_particles()
        
        # Update trails
        self._update_trails(keypoints)
    
    def _handle_gestures(self, keypoints: Dict, gestures: List[str], energy: float):
        """Create effects for specific gestures"""
        
        if 'hands_up' in gestures:
            # Particle explosion from hands
            for hand in ['left_wrist', 'right_wrist']:
                if hand in keypoints:
                    self._create_explosion(keypoints[hand][0], keypoints[hand][1], 
                                         self.energetic_colors)
        
        if 'arms_wide' in gestures:
            # Create connecting line particles
            if 'left_wrist' in keypoints and 'right_wrist' in keypoints:
                self._create_line_particles(keypoints['left_wrist'], 
                                          keypoints['right_wrist'], 
                                          self.calm_colors)
        
        if 'jump' in gestures:
            # Fireworks burst
            if 'hip_center' in keypoints:
                self._create_fireworks(keypoints['hip_center'][0], 
                                     keypoints['hip_center'][1] - 100)
    
    def _create_ambient_particles(self, keypoints: Dict, energy: float):
        """Create ambient particles following key points"""
        if energy < 1:
            return
        
        # Hands create trailing particles
        for hand in ['left_wrist', 'right_wrist']:
            if hand in keypoints and random.random() < energy / 10:
                x, y = keypoints[hand]
                color = random.choice(self._get_color_palette(energy))
                
                # Add some randomness
                x += random.randint(-10, 10)
                y += random.randint(-10, 10)
                
                particle = Particle(x, y, 
                                   random.uniform(-2, 2), 
                                   random.uniform(-3, 1),
                                   color, 
                                   random.uniform(0.5, 1.5),
                                   random.uniform(2, 5))
                self.particles.append(particle)
    
    def _create_explosion(self, x: int, y: int, colors: List[Tuple[int, int, int]]):
        """Create particle explosion at given position"""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = random.choice(colors)
            particle = Particle(x, y, vx, vy, color, 
                               random.uniform(1.0, 2.0),
                               random.uniform(3, 6))
            self.particles.append(particle)
    
    def _create_line_particles(self, start: Tuple[int, int], end: Tuple[int, int], 
                              colors: List[Tuple[int, int, int]]):
        """Create particles along a line between two points"""
        steps = 10
        for i in range(steps):
            t = i / steps
            x = int(start[0] * (1 - t) + end[0] * t)
            y = int(start[1] * (1 - t) + end[1] * t)
            
            color = random.choice(colors)
            particle = Particle(x, y, 
                               random.uniform(-1, 1), 
                               random.uniform(-2, 0),
                               color, 
                               random.uniform(0.8, 1.2),
                               random.uniform(2, 4))
            self.particles.append(particle)
    
    def _create_fireworks(self, x: int, y: int):
        """Create fireworks burst effect"""
        for _ in range(25):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 12)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = random.choice(self.energetic_colors)
            particle = Particle(x, y, vx, vy, color, 
                               random.uniform(1.5, 2.5),
                               random.uniform(4, 7))
            self.particles.append(particle)
    
    def _update_particles(self):
        """Update all particles and remove dead ones"""
        for particle in self.particles[:]:
            particle.update()
            if particle.is_dead() or particle.y > self.height + 50:
                self.particles.remove(particle)
    
    def _update_trails(self, keypoints: Dict):
        """Update hand trails"""
        # Add current hand positions to trails
        for hand in ['left_wrist', 'right_wrist']:
            if hand in keypoints:
                # Create trail data structure if needed
                if not hasattr(self, f'{hand}_trail'):
                    setattr(self, f'{hand}_trail', [])
                
                trail = getattr(self, f'{hand}_trail')
                trail.append(keypoints[hand])
                
                # Keep trail length manageable
                if len(trail) > 15:
                    trail.pop(0)
    
    def _get_color_palette(self, energy: float) -> List[Tuple[int, int, int]]:
        """Get color palette based on energy level"""
        if energy < 2:
            return self.calm_colors
        elif energy > 6:
            return self.energetic_colors
        else:
            return self.neutral_colors
    
    def draw(self, screen):
        """Draw all visual effects"""
        # Dynamic background
        bg_color = (int(self.background_intensity * 0.1), 
                   int(self.background_intensity * 0.05), 
                   int(self.background_intensity * 0.15))
        screen.fill(bg_color)
        
        # Draw geometric background pattern
        self._draw_background_pattern(screen)
        
        # Draw trails
        self._draw_trails(screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
        
        # Draw connecting lines between key joints
        self._draw_skeleton_effects(screen)
    
    def _draw_background_pattern(self, screen):
        """Draw animated background pattern"""
        if self.background_intensity > 30:
            # Draw pulsing circles
            center_x, center_y = self.width // 2, self.height // 2
            radius = int(self.background_intensity * 2)
            
            for i in range(3):
                alpha = max(0, int(self.background_intensity - i * 30))
                color = (alpha // 3, alpha // 6, alpha // 2)
                if alpha > 0:
                    pygame.draw.circle(screen, color, 
                                     (center_x, center_y), 
                                     radius + i * 50, 2)
    
    def _draw_trails(self, screen):
        """Draw hand trails"""
        for hand in ['left_wrist', 'right_wrist']:
            if hasattr(self, f'{hand}_trail'):
                trail = getattr(self, f'{hand}_trail')
                if len(trail) > 1:
                    # Draw trail with fading effect
                    for i in range(1, len(trail)):
                        alpha = i / len(trail)
                        color = (int(255 * alpha), int(200 * alpha), int(100 * alpha))
                        start_pos = trail[i-1]
                        end_pos = trail[i]
                        pygame.draw.line(screen, color, start_pos, end_pos, 3)
    
    def _draw_skeleton_effects(self, screen):
        """Draw effects connecting skeleton joints"""
        # This could connect major joints with glowing lines
        # Implementation depends on current pose data
        pass
