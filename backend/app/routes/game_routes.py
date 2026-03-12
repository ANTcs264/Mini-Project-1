from flask import Blueprint, request, jsonify
from app.models.player import PlayerManager
from app.models.story import StoryManager
from app.ml.classifier import PersonalityClassifier
from app.story_engine.generator import StoryGenerator
import random

game_bp = Blueprint('game', __name__)

# Initialize components
player_manager = PlayerManager()
story_manager = StoryManager()
classifier = PersonalityClassifier()
story_gen = StoryGenerator()

@game_bp.route('/start', methods=['POST'])
def start_game():
    """Start a new game session"""
    try:
        # Create new player session
        session_id = player_manager.create_new_session()
        
        # Get start story node
        start_node = story_gen.get_start_node()
        
        # Initialize story state
        story_manager.update_story_state(session_id, 'start', [])
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'story': start_node
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@game_bp.route('/choice', methods=['POST'])
def make_choice():
    """Process player's choice and return next story segment"""
    try:
        data = request.json
        session_id = data.get('session_id')
        choice_id = data.get('choice_id')
        current_node_id = data.get('current_node_id')
        
        if not all([session_id, choice_id, current_node_id]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Get the current node to find the choice
        current_node = story_gen.get_node(current_node_id)
        if not current_node:
            return jsonify({'success': False, 'error': 'Invalid node ID'}), 400
        
        # Find the chosen option
        chosen_option = None
        for choice in current_node.get('choices', []):
            if choice['id'] == choice_id:
                chosen_option = choice
                break
        
        if not chosen_option:
            return jsonify({'success': False, 'error': 'Invalid choice ID'}), 400
        
        # Record player action
        player_manager.record_action(
            session_id,
            chosen_option['action_type'],
            chosen_option['text'],
            current_node_id
        )
        
        # Get player features for personality prediction
        features = player_manager.get_player_features(session_id)
        
        # Predict personality
        personality = classifier.predict_personality(features)
        
        # Update player session with personality
        session = player_manager.get_session(session_id)
        if session:
            session.personality_type = personality
            from app import db
            db.session.commit()
        
        # Get next story node (adapted based on personality)
        next_node_id = chosen_option['next_node']
        next_node = story_gen.get_adapted_node(next_node_id, personality, chosen_option['action_type'])
        
        # Update story state
        story_state = story_manager.get_story_state(session_id)
        history = story_state['history'] if story_state else []
        history.append({
            'node': current_node_id,
            'choice': chosen_option['text'],
            'personality_at_time': personality
        })
        story_manager.update_story_state(session_id, next_node_id, history)
        
        # Get player stats for display
        stats = {
            'fights': session.total_fights,
            'diplomatic': session.total_diplomatic,
            'stealth': session.total_stealth,
            'risky': session.total_risky,
            'cautious': session.total_cautious,
            'personality': personality
        }
        
        return jsonify({
            'success': True,
            'story': next_node,
            'stats': stats,
            'personality': personality
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@game_bp.route('/stats/<session_id>', methods=['GET'])
def get_stats(session_id):
    """Get player statistics"""
    try:
        session = player_manager.get_session(session_id)
        if not session:
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        stats = {
            'fights': session.total_fights,
            'diplomatic': session.total_diplomatic,
            'stealth': session.total_stealth,
            'risky': session.total_risky,
            'cautious': session.total_cautious,
            'personality': session.personality_type,
            'total_actions': (session.total_fights + session.total_diplomatic + 
                            session.total_stealth + session.total_risky + 
                            session.total_cautious)
        }
        
        return jsonify({'success': True, 'stats': stats}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500