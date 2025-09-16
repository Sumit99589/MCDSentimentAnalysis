document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const commentsInput = document.getElementById('comments-input');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    
    analyzeBtn.addEventListener('click', async function() {
        console.log('Analyze button clicked'); // Debug
        
        const commentsText = commentsInput.value.trim();
        let comments = [];
        
        if (commentsText) {
            comments = commentsText.split('\n').filter(c => c.trim());
        }
        
        console.log('Comments to analyze:', comments); // Debug
        
        loading.classList.remove('hidden');
        results.classList.add('hidden');
        analyzeBtn.disabled = true;
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comments: comments })
            });
            
            console.log('Response status:', response.status); // Debug
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Response data:', data); // Debug
            
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            displayResults(data);
            
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while analyzing comments: ' + error.message);
        } finally {
            loading.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });
    
    function displayResults(data) {
        console.log('Displaying results:', data); // Debug
        
        createSentimentChart(data.sentiment_distribution);
        displaySentimentStats(data.sentiment_distribution, data.total_comments);
        
        // Show simple word cloud message instead of image
        const wordcloudImg = document.getElementById('wordcloud-image');
        wordcloudImg.style.display = 'none';
        wordcloudImg.parentElement.innerHTML = '<p class="text-gray-600">Word frequency analysis completed. Top words: ' + 
            Object.keys(data.wordcloud_data).slice(0, 5).join(', ') + '</p>';
        
        displayIndividualResults(data.individual_results);
        
        results.classList.remove('hidden');
    }
    
    function createSentimentChart(sentimentData) {
        const ctx = document.getElementById('sentiment-chart').getContext('2d');
        
        const labels = Object.keys(sentimentData);
        const values = Object.values(sentimentData);
        const colors = {
            'positive': '#10B981',
            'negative': '#EF4444',
            'neutral': '#6B7280'
        };
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels.map(l => l.charAt(0).toUpperCase() + l.slice(1)),
                datasets: [{
                    data: values,
                    backgroundColor: labels.map(label => colors[label] || '#6B7280')
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    function displaySentimentStats(sentimentData, total) {
        const statsContainer = document.getElementById('sentiment-stats');
        
        let html = `<h3 class="text-lg font-semibold mb-3">Analysis Summary</h3>`;
        html += `<p class="text-gray-600 mb-4">Total Comments Analyzed: <span class="font-semibold">${total}</span></p>`;
        
        for (const [sentiment, count] of Object.entries(sentimentData)) {
            const percentage = ((count / total) * 100).toFixed(1);
            const colorClass = sentiment === 'positive' ? 'text-green-600' : 
                              sentiment === 'negative' ? 'text-red-600' : 'text-gray-600';
            
            html += `
                <div class="flex justify-between items-center py-2 border-b">
                    <span class="capitalize font-medium">${sentiment}</span>
                    <span class="${colorClass} font-semibold">${count} (${percentage}%)</span>
                </div>
            `;
        }
        
        statsContainer.innerHTML = html;
    }
    
    function displayIndividualResults(results) {
        const container = document.getElementById('individual-results');
        
        let html = '';
        results.forEach((result, index) => {
            const sentimentColor = result.sentiment === 'positive' ? 'green' : 
                                  result.sentiment === 'negative' ? 'red' : 'gray';
            
            html += `
                <div class="border border-gray-200 rounded-lg p-4">
                    <div class="flex justify-between items-start mb-3">
                        <h4 class="font-semibold text-gray-800">Comment ${index + 1}</h4>
                        <div class="flex items-center space-x-2">
                            <span class="px-2 py-1 rounded text-sm bg-${sentimentColor}-100 text-${sentimentColor}-800">
                                ${result.sentiment.charAt(0).toUpperCase() + result.sentiment.slice(1)}
                            </span>
                            <span class="text-sm text-gray-500">
                                Confidence: ${(result.confidence * 100).toFixed(1)}%
                            </span>
                        </div>
                    </div>
                    <p class="text-gray-700 mb-3">${result.comment}</p>
                    <div class="bg-blue-50 rounded p-3">
                        <h5 class="font-medium text-blue-800 mb-1">Summary:</h5>
                        <p class="text-blue-700 text-sm">${result.summary}</p>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }
});
