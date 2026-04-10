let currentSessionId = null;
let currentStory = null;

const storyText = document.getElementById('story-text');
const storyImage = document.getElementById('story-image');
const choicesGrid = document.getElementById('choices-grid');
const newGameBtn = document.getElementById('new-game-btn');
const personalityEl = document.getElementById('personality');
const fightsEl = document.getElementById('fights');
const diplomaticEl = document.getElementById('diplomatic');
const stealthEl = document.getElementById('stealth');
const riskyEl = document.getElementById('risky');
const cautiousEl = document.getElementById('cautious');
const totalActionsEl = document.getElementById('total-actions');

newGameBtn.addEventListener('click', startNewGame);

async function startNewGame() {
    try {
        storyText.innerText = 'Starting new game...';
        choicesGrid.innerHTML = '<div class="loading"></div>';
        
        const data = await api.startNewGame();
        console.log('API response:', data);
        
        if (data.success) {
            currentSessionId = data.session_id;
            currentStory = data.story;
            displayStory(currentStory);
            updateStats({
                fights: 0, diplomatic: 0, stealth: 0, risky: 0, cautious: 0,
                personality: 'UNCLASSIFIED'
            });
        } else {
            storyText.innerText = 'Error: ' + (data.error || 'Unknown error');
            choicesGrid.innerHTML = '';
        }
    } catch (error) {
        console.error('Error starting game:', error);
        storyText.innerText = 'Network error: Cannot reach backend on port 5000.';
        choicesGrid.innerHTML = '';
    }
}

function displayStory(story) {
    if (!story) return;
    storyText.innerText = story.text;
    if (story.image) {
        storyImage.style.backgroundImage = `url(assets/images/${story.image})`;
        storyImage.style.backgroundSize = 'cover';
        storyImage.style.backgroundPosition = 'center';
    }
    choicesGrid.innerHTML = '';
    if (story.choices && story.choices.length > 0) {
        story.choices.forEach(choice => {
            const btn = document.createElement('button');
            btn.className = 'choice-btn';
            btn.innerHTML = `<span class="choice-icon">${getIcon(choice.action_type)}</span>
                             <span class="choice-text">${choice.text}</span>`;
            btn.addEventListener('click', () => makeChoice(choice.id));
            choicesGrid.appendChild(btn);
        });
    } else {
        choicesGrid.innerHTML = '<div class="no-choices">The adventure continues...</div>';
    }
}

function getIcon(type) {
    const icons = { fight:'⚔️', diplomatic:'🤝', stealth:'👤', risky:'⚡', cautious:'🛡️' };
    return icons[type] || '🎯';
}

async function makeChoice(choiceId) {
    if (!currentSessionId || !currentStory) return;
    try {
        const data = await api.makeChoice(currentSessionId, choiceId, currentStory.id);
        if (data.success) {
            currentStory = data.story;
            displayStory(currentStory);
            if (data.stats) updateStats(data.stats);
        } else {
            storyText.innerText = 'Error making choice: ' + (data.error || 'Unknown');
        }
    } catch (error) {
        console.error('Error making choice:', error);
        storyText.innerText = 'Network error while making choice.';
    }
}

function updateStats(stats) {
    fightsEl.innerText = stats.fights || 0;
    diplomaticEl.innerText = stats.diplomatic || 0;
    stealthEl.innerText = stats.stealth || 0;
    riskyEl.innerText = stats.risky || 0;
    cautiousEl.innerText = stats.cautious || 0;
    personalityEl.innerText = stats.personality || 'UNCLASSIFIED';
    const total = (stats.fights||0)+(stats.diplomatic||0)+(stats.stealth||0)+(stats.risky||0)+(stats.cautious||0);
    totalActionsEl.innerText = total;
}

// Start automatically when page loads
startNewGame();