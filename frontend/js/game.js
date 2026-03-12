// Game state
let currentSessionId = null;
let currentStory = null;
let playerStats = {
    fights: 0,
    diplomatic: 0,
    stealth: 0,
    risky: 0,
    cautious: 0,
    personality: 'UNCLASSIFIED'
};

// DOM Elements
const storyText = document.getElementById('story-text');
const storyImage = document.getElementById('story-image');
const choicesGrid = document.getElementById('choices-grid');
const newGameBtn = document.getElementById('new-game-btn');
const achievementPopup = document.getElementById('achievement-popup');
const achievementDesc = document.getElementById('achievement-desc');

// Stats elements
const statsElements = {
    fights: document.getElementById('fights'),
    diplomatic: document.getElementById('diplomatic'),
    stealth: document.getElementById('stealth'),
    risky: document.getElementById('risky'),
    cautious: document.getElementById('cautious'),
    personality: document.getElementById('personality'),
    totalActions: document.getElementById('total-actions'),
    personalityConfidence: document.getElementById('personality-confidence')
};

// Progress bars
const progressBars = {
    fights: document.querySelector('.fights-bar'),
    diplomatic: document.querySelector('.diplomatic-bar'),
    stealth: document.querySelector('.stealth-bar'),
    risky: document.querySelector('.risky-bar'),
    cautious: document.querySelector('.cautious-bar')
};

// Event listeners
newGameBtn.addEventListener('click', startNewGame);

// Initialize game on page load
document.addEventListener('DOMContentLoaded', () => {
    startNewGame();
    setupParticles();
});

// Start new game
async function startNewGame() {
    try {
        // Show loading state
        storyText.innerHTML = '<div class="typing-effect">Initializing new adventure...</div>';
        choicesGrid.innerHTML = '<div class="loading"></div>';
        
        const data = await api.startNewGame();
        
        if (data.success) {
            currentSessionId = data.session_id;
            currentStory = data.story;
            
            // Reset stats
            playerStats = {
                fights: 0,
                diplomatic: 0,
                stealth: 0,
                risky: 0,
                cautious: 0,
                personality: 'UNCLASSIFIED'
            };
            
            updateStats();
            displayStory(currentStory);
            showAchievement('New Adventure Begins!');
            
            // Update game status
            document.querySelector('.status-dot').style.background = '#00ff00';
            document.getElementById('game-status').querySelector('span').textContent = 'IN GAME';
        }
    } catch (error) {
        console.error('Error starting game:', error);
        storyText.innerHTML = 'Error starting game. Please try again.';
    }
}

// Display story
function displayStory(story) {
    if (!story) return;
    
    // Typewriter effect for story text
    typeWriter(story.text, storyText);
    
    // Set story image with fade effect
    if (story.image) {
        storyImage.style.backgroundImage = `url(assets/images/${story.image})`;
        storyImage.style.opacity = '0';
        setTimeout(() => {
            storyImage.style.transition = 'opacity 1s';
            storyImage.style.opacity = '1';
        }, 100);
    }
    
    // Display choices
    displayChoices(story.choices || []);
}

// Typewriter effect
function typeWriter(text, element, speed = 30) {
    let i = 0;
    element.innerHTML = '';
    element.classList.add('typing-effect');
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        } else {
            element.classList.remove('typing-effect');
        }
    }
    
    type();
}

// Display choices with animations
function displayChoices(choices) {
    if (!choices || choices.length === 0) {
        choicesGrid.innerHTML = '<div class="no-choices">No choices available</div>';
        return;
    }
    
    choicesGrid.innerHTML = '';
    
    choices.forEach((choice, index) => {
        const button = document.createElement('button');
        button.className = 'choice-btn';
        button.style.animation = `slideIn 0.3s ease ${index * 0.1}s forwards`;
        button.innerHTML = `
            <span class="choice-icon">${getChoiceIcon(choice.action_type)}</span>
            <span class="choice-text">${choice.text}</span>
            <span class="choice-type">${choice.action_type.toUpperCase()}</span>
        `;
        
        button.addEventListener('click', () => makeChoice(choice.id));
        
        choicesGrid.appendChild(button);
    });
}

// Get icon for choice type
function getChoiceIcon(type) {
    const icons = {
        fight: '⚔️',
        diplomatic: '🤝',
        stealth: '👤',
        risky: '⚡',
        cautious: '🛡️',
        default: '🎯'
    };
    return icons[type] || icons.default;
}

// Make a choice
async function makeChoice(choiceId) {
    if (!currentSessionId || !currentStory) return;
    
    try {
        // Disable all choice buttons temporarily
        document.querySelectorAll('.choice-btn').forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
        });
        
        const data = await api.makeChoice(currentSessionId, choiceId, currentStory.id);
        
        if (data.success) {
            // Update story
            currentStory = data.story;
            
            // Update stats
            if (data.stats) {
                playerStats = data.stats;
                updateStats();
            }
            
            // Show achievement for personality detection
            if (data.personality && data.personality !== 'UNCLASSIFIED' && 
                playerStats.personality !== data.personality) {
                showAchievement(`Personality Detected: ${data.personality}`);
            }
            
            // Display next story segment
            displayStory(currentStory);
            
            // Show action feedback
            showActionFeedback(data.story.choices[0]?.action_type);
        }
    } catch (error) {
        console.error('Error making choice:', error);
        storyText.innerHTML += '<br><span style="color: #ff4444">Error processing choice. Please try again.</span>';
    }
}

// Update stats display
function updateStats() {
    // Update numeric values
    statsElements.fights.textContent = playerStats.fights || 0;
    statsElements.diplomatic.textContent = playerStats.diplomatic || 0;
    statsElements.stealth.textContent = playerStats.stealth || 0;
    statsElements.risky.textContent = playerStats.risky || 0;
    statsElements.cautious.textContent = playerStats.cautious || 0;
    
    // Update personality
    statsElements.personality.textContent = playerStats.personality || 'UNCLASSIFIED';
    
    // Update total actions
    const total = (playerStats.fights || 0) + (playerStats.diplomatic || 0) + 
                  (playerStats.stealth || 0) + (playerStats.risky || 0) + 
                  (playerStats.cautious || 0);
    statsElements.totalActions.textContent = total;
    
    // Update progress bars
    const maxStat = Math.max(
        playerStats.fights || 0,
        playerStats.diplomatic || 0,
        playerStats.stealth || 0,
        playerStats.risky || 0,
        playerStats.cautious || 0,
        1
    );
    
    progressBars.fights.style.width = `${(playerStats.fights || 0) / maxStat * 100}%`;
    progressBars.diplomatic.style.width = `${(playerStats.diplomatic || 0) / maxStat * 100}%`;
    progressBars.stealth.style.width = `${(playerStats.stealth || 0) / maxStat * 100}%`;
    progressBars.risky.style.width = `${(playerStats.risky || 0) / maxStat * 100}%`;
    progressBars.cautious.style.width = `${(playerStats.cautious || 0) / maxStat * 100}%`;
    
    // Update personality confidence bar
    const confidence = playerStats.personality !== 'UNCLASSIFIED' ? 80 : 20;
    statsElements.personalityConfidence.style.width = `${confidence}%`;
    
    // Change personality color based on type
    const personalityEl = statsElements.personality;
    personalityEl.style.color = getPersonalityColor(playerStats.personality);
}

// Get color for personality type
function getPersonalityColor(personality) {
    const colors = {
        'AGGRESSIVE': '#ff4444',
        'DIPLOMATIC': '#44ff44',
        'STEALTHY': '#4444ff',
        'BALANCED': '#ffaa44',
        'UNCLASSIFIED': '#ffffff'
    };
    return colors[personality] || colors.UNCLASSIFIED;
}

// Show achievement popup
function showAchievement(message) {
    achievementDesc.textContent = message;
    achievementPopup.classList.addEventListener('animationend', () => {
        achievementPopup.classList.remove('show');
    });
    achievementPopup.classList.add('show');
}   