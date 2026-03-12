import json
import os
import random

class StoryGenerator:
    def __init__(self):
        """Initialize story generator with story data"""
        story_path = os.path.join(os.path.dirname(__file__), 'story_data.json')
        with open(story_path, 'r') as f:
            self.story_data = json.load(f)['nodes']
    
    def get_start_node(self):
        """Get the starting story node"""
        return self.story_data['start']
    
    def get_node(self, node_id):
        """Get a specific story node by ID"""
        return self.story_data.get(node_id, self.story_data['start'])
    
    def get_adapted_node(self, node_id, personality_type, last_action_type=None):
        """
        Get a story node, potentially adapted based on personality
        For MVP, this filters choices based on personality
        """
        node = self.get_node(node_id)
        
        if not node:
            return self.get_start_node()
        
        # Create a copy to modify
        adapted_node = node.copy()
        
        # Filter choices based on personality (if not at end node)
        if node_id != 'end' and 'choices' in adapted_node:
            choices = adapted_node['choices']
            
            # Prioritize choices that match personality
            personality_lower = personality_type.lower()
            matching_choices = [c for c in choices if personality_lower in c.get('tags', [])]
            
            # If we have matching choices, put them first
            if matching_choices and len(matching_choices) < len(choices):
                other_choices = [c for c in choices if personality_lower not in c.get('tags', [])]
                adapted_node['choices'] = matching_choices + other_choices
            
            # Add personality-specific flavor to text
            if personality_type == 'AGGRESSIVE':
                adapted_node['text'] += " Your aggressive nature drives you forward."
            elif personality_type == 'DIPLOMATIC':
                adapted_node['text'] += " Your diplomatic instincts guide your choices."
            elif personality_type == 'STEALTHY':
                adapted_node['text'] += " You instinctively look for shadows and hiding spots."
        
        return adapted_node