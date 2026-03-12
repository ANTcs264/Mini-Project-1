from app import db
from app.models.database import StoryState
import json

class StoryManager:
    @staticmethod
    def update_story_state(session_id, current_node, story_history):
        """Update player's story state"""
        story_state = StoryState.query.filter_by(session_id=session_id).first()
        
        if not story_state:
            story_state = StoryState(
                session_id=session_id,
                current_story_node=current_node,
                story_history=json.dumps(story_history)
            )
            db.session.add(story_state)
        else:
            story_state.current_story_node = current_node
            story_state.story_history = json.dumps(story_history)
        
        db.session.commit()
        return story_state
    
    @staticmethod
    def get_story_state(session_id):
        """Get player's current story state"""
        story_state = StoryState.query.filter_by(session_id=session_id).first()
        if story_state:
            return {
                'current_node': story_state.current_story_node,
                'history': json.loads(story_state.story_history) if story_state.story_history else []
            }
        return None