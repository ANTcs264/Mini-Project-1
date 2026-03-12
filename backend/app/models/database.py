from app import db

class PlayerSession(db.Model):
    __tablename__ = 'player_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_active = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Player stats
    total_fights = db.Column(db.Integer, default=0)
    total_diplomatic = db.Column(db.Integer, default=0)
    total_stealth = db.Column(db.Integer, default=0)
    total_risky = db.Column(db.Integer, default=0)
    total_cautious = db.Column(db.Integer, default=0)
    
    # Predicted personality
    personality_type = db.Column(db.String(50), default='UNCLASSIFIED')
    
    # Relationships
    actions = db.relationship('PlayerAction', backref='session', lazy=True)
    story_states = db.relationship('StoryState', backref='session', lazy=True)

class PlayerAction(db.Model):
    __tablename__ = 'player_actions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), db.ForeignKey('player_sessions.session_id'))
    action_type = db.Column(db.String(50))  # fight, diplomatic, stealth, risky, cautious
    action_description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    story_node_id = db.Column(db.String(50))

class StoryState(db.Model):
    __tablename__ = 'story_states'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), db.ForeignKey('player_sessions.session_id'))
    current_story_node = db.Column(db.String(50))
    story_history = db.Column(db.Text)  # JSON string of story path
    last_updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())