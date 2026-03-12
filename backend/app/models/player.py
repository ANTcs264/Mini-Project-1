import uuid
from app import db
from app.models.database import PlayerSession, PlayerAction

class PlayerManager:
    @staticmethod
    def create_new_session():
        """Create a new player session"""
        session_id = str(uuid.uuid4())
        new_session = PlayerSession(session_id=session_id)
        db.session.add(new_session)
        db.session.commit()
        return session_id
    
    @staticmethod
    def get_session(session_id):
        """Get player session by ID"""
        return PlayerSession.query.filter_by(session_id=session_id).first()
    
    @staticmethod
    def record_action(session_id, action_type, action_description, story_node_id):
        """Record player action"""
        session = PlayerManager.get_session(session_id)
        if not session:
            return False
        
        # Update session stats
        if action_type == 'fight':
            session.total_fights += 1
        elif action_type == 'diplomatic':
            session.total_diplomatic += 1
        elif action_type == 'stealth':
            session.total_stealth += 1
        elif action_type == 'risky':
            session.total_risky += 1
        elif action_type == 'cautious':
            session.total_cautious += 1
        
        # Create action record
        action = PlayerAction(
            session_id=session_id,
            action_type=action_type,
            action_description=action_description,
            story_node_id=story_node_id
        )
        
        db.session.add(action)
        db.session.commit()
        return True
    
    @staticmethod
    def get_player_features(session_id):
        """Get numerical features for ML model"""
        session = PlayerManager.get_session(session_id)
        if not session:
            return None
        
        features = [
            session.total_fights,
            session.total_diplomatic,
            session.total_stealth,
            session.total_risky,
            session.total_cautious
        ]
        return features