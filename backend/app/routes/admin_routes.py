from flask import Blueprint, jsonify
from app.models.database import PlayerSession, PlayerAction
from app import db
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
def get_game_stats():
    """Get overall game statistics"""
    try:
        # Total players
        total_players = PlayerSession.query.count()
        
        # Personality distribution
        personality_counts = db.session.query(
            PlayerSession.personality_type, 
            func.count(PlayerSession.personality_type)
        ).group_by(PlayerSession.personality_type).all()
        
        personality_dist = {p: count for p, count in personality_counts if p}
        
        # Total actions
        total_actions = PlayerAction.query.count()
        
        # Action distribution
        action_counts = db.session.query(
            PlayerAction.action_type,
            func.count(PlayerAction.action_type)
        ).group_by(PlayerAction.action_type).all()
        
        action_dist = {a: count for a, count in action_counts}
        
        return jsonify({
            'success': True,
            'stats': {
                'total_players': total_players,
                'personality_distribution': personality_dist,
                'total_actions': total_actions,
                'action_distribution': action_dist
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500