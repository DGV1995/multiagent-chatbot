class Chatbot {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatHistory = [];
        this.apiUrl = 'http://localhost:8000';
        
        this.init();
    }
    
    init() {
        // Set initial time
        document.getElementById('initialTime').textContent = this.getCurrentTime();
        
        // Event listeners
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Focus on input
        this.messageInput.focus();
    }
    
    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Disable input while processing
        this.setInputEnabled(false);
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        
        // Show loading indicator
        const loadingElement = this.addLoadingMessage();
        
        try {
            // Send request to backend
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    history: this.chatHistory
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Remove loading indicator
            this.removeLoadingMessage(loadingElement);
            
            if (data.success) {
                // Add bot response to chat
                this.addMessage(data.response, 'bot');
                
                // Update chat history
                this.chatHistory.push({
                    user: message,
                    assistant: data.response
                });
            } else {
                this.addMessage('Sorry, I encountered an error processing your request.', 'bot', true);
            }
            
        } catch (error) {
            console.error('Error:', error);
            
            // Remove loading indicator
            this.removeLoadingMessage(loadingElement);
            
            // Show error message
            let errorMessage = 'Sorry, I\'m having trouble connecting to the server. ';
            if (error.message.includes('Failed to fetch')) {
                errorMessage += 'Please make sure the backend server is running on http://localhost:8000';
            } else {
                errorMessage += 'Please try again later.';
            }
            
            this.addMessage(errorMessage, 'bot', true);
        } finally {
            // Re-enable input
            this.setInputEnabled(true);
            this.messageInput.focus();
        }
    }
    
    addMessage(content, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;
        
        if (isError) {
            contentDiv.style.color = '#dc3545';
        }
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.getCurrentTime();
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addLoadingMessage() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.id = 'loading-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content loading';
        
        contentDiv.innerHTML = `
            <span>Thinking</span>
            <div class="loading-dots">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
        `;
        
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageDiv;
    }
    
    removeLoadingMessage(loadingElement) {
        if (loadingElement && loadingElement.parentNode) {
            loadingElement.parentNode.removeChild(loadingElement);
        }
    }
    
    setInputEnabled(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        
        if (enabled) {
            this.sendButton.textContent = 'Send';
        } else {
            this.sendButton.textContent = 'Sending...';
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new Chatbot();
});