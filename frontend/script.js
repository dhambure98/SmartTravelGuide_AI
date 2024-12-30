document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const searchForm = document.getElementById('searchForm');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('errorMessage');
    const recommendationsContainer = document.getElementById('recommendationsContainer');
    const submitBtn = document.getElementById('submitBtn');

    // Backend API URL
    const API_URL = 'http://localhost:5001/api/recommend';

    // Form submit handler
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        loading.style.display = 'block';
        errorMessage.style.display = 'none';
        recommendationsContainer.innerHTML = '';
        submitBtn.disabled = true;

        // Get form values
        const preferences = document.getElementById('preferences').value;
        const age = document.getElementById('age').value;
        const minBudget = document.getElementById('minBudget').value;
        const maxBudget = document.getElementById('maxBudget').value;

        // Validation
        if (!preferences || !age || !minBudget || !maxBudget) {
            showError('Please fill out all fields.');
            loading.style.display = 'none';
            submitBtn.disabled = false;
            return;
        }

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    preferences: preferences,
                    age: parseInt(age),
                    budget_range: [parseInt(minBudget), parseInt(maxBudget)]
                })
            });

            const data = await response.json();

            if (data.recommendations) {
                displayRecommendations(data.recommendations);
            } else {
                showError(data.error || 'Failed to get recommendations');
            }
        } catch (err) {
            showError('Failed to connect to the server');
        } finally {
            loading.style.display = 'none';
            submitBtn.disabled = false;
        }
    });

    // Display recommendations
    function displayRecommendations(recommendations) {
        recommendationsContainer.innerHTML = '<h2 style="margin-bottom: 20px; color: #2c3e50; font-size: 1.8em;">Recommended Destinations</h2>';

        recommendations.forEach(recommendation => {
            const card = createRecommendationCard(recommendation);
            recommendationsContainer.appendChild(card);
        });
    }

    // Create recommendation card
    function createRecommendationCard(recommendation) {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        
        card.innerHTML = `
            <div class="destination-header">
                <div>
                    <h3 class="destination-name">${recommendation.name}</h3>
                    <p class="destination-region">${recommendation.region}</p>
                </div>
                <span class="popularity">★ ${recommendation.popularity.toFixed(1)}</span>
            </div>
            <div class="details">
                <div class="detail-item">
                    <i>📅</i>
                    <span>Best Season: ${recommendation.best_season}</span>
                </div>
                <div class="detail-item">
                    <i>💰</i>
                    <span>Budget: $${recommendation.budget.toLocaleString()}</span>
                </div>
            </div>
            <div class="attractions">
                <h4 style="color: #2c3e50; margin-bottom: 8px;">Attractions:</h4>
                <p>${recommendation.attractions}</p>
            </div>
            <div class="match-score">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Match Score</span>
                    <span>${(recommendation.match_score * 100).toFixed(0)}%</span>
                </div>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${recommendation.match_score * 100}%"></div>
                </div>
            </div>
        `;
        
        return card;
    }

    // Show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }
});
