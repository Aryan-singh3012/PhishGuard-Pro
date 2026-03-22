document.addEventListener('DOMContentLoaded', function() {
    const statusBox = document.getElementById('status'); // Ensure this ID exists in popup.html
    const riskBar = document.getElementById('risk-bar');
    const reasonsBox = document.getElementById('reasons');
    const urlText = document.getElementById('current-url');

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let activeTab = tabs[0];
        if (activeTab) {
            urlText.textContent = activeTab.url;

            // Call your local FastAPI backend
            fetch('http://127.0.0.1:8000/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    url: activeTab.url,
                    title: activeTab.title || ""
                })
            })
            .then(res => res.json())
            .then(data => {
                // Update the UI with real data from FastAPI
                statusBox.textContent = data.status;
                statusBox.className = data.status === "PHISHING" ? "status-box danger" : "status-box safe";
                
                riskBar.style.width = data.risk_score + "%";
                riskBar.style.backgroundColor = data.risk_score > 70 ? "#ef4444" : "#10b981";
                
                reasonsBox.innerHTML = `<b>Reason:</b> ${data.reasons}`;
            })
            .catch(error => {
                console.error('Error:', error);
                statusBox.textContent = "❌ ENGINE OFFLINE";
                statusBox.className = "status-box danger";
            });
        }
    });

    // Secure click handler for the button
    document.getElementById('reScanBtn').addEventListener('click', function() {
        window.location.reload();
    });
});