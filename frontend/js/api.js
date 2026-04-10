// Use relative path on Vercel, localhost for development
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000/api/game'
    : '/api/game';

const api = {
    async startNewGame() {
        const response = await fetch(`${API_BASE_URL}/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        return response.json();
    },

    async makeChoice(sessionId, choiceId, currentNodeId) {
        const response = await fetch(`${API_BASE_URL}/choice`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                choice_id: choiceId,
                current_node_id: currentNodeId
            })
        });
        return response.json();
    },

    async getStats(sessionId) {
        const response = await fetch(`${API_BASE_URL}/stats/${sessionId}`);
        return response.json();
    }
};