import React, { useState, useRef, useEffect } from 'react';
import ChatBubble from './components/ChatBubble';
import SourceList from './components/SourceList';
import { askQuestion } from './api';
import { Send, Sparkles } from 'lucide-react';

function App() {
    const [messages, setMessages] = useState([
        { id: 1, sender: 'bot', text: 'Hello! I am NLPAssist+. How can I help you today?' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = { id: Date.now(), sender: 'user', text: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await askQuestion(userMessage.text);

            const botMessage = {
                id: Date.now() + 1,
                sender: 'bot',
                text: response.answer,
                sources: response.sources
            };

            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            const errorMessage = {
                id: Date.now() + 1,
                sender: 'bot',
                text: "Sorry, I encountered an error. Please try again later."
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen bg-gray-900 text-gray-100 flex-col font-inter">
            {/* Header */}
            <header className="p-4 border-b border-gray-800 bg-gray-900/50 backdrop-blur sticky top-0 z-10">
                <div className="max-w-4xl mx-auto flex items-center gap-2">
                    <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                        <Sparkles size={18} className="text-white" />
                    </div>
                    <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
                        NLPAssist+
                    </h1>
                </div>
            </header>

            {/* Chat Area */}
            <main className="flex-1 overflow-y-auto p-4">
                <div className="max-w-4xl mx-auto space-y-6">
                    {messages.map((msg) => (
                        <div key={msg.id}>
                            <ChatBubble message={msg} />
                            {msg.sender === 'bot' && msg.sources && (
                                <SourceList sources={msg.sources} />
                            )}
                        </div>
                    ))}

                    {loading && (
                        <div className="flex justify-start mb-4 pl-12">
                            <div className="flex space-x-2 bg-gray-800 p-3 rounded-2xl rounded-tl-none items-center">
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </main>

            {/* Input Area */}
            <div className="p-4 border-t border-gray-800 bg-gray-900">
                <div className="max-w-4xl mx-auto">
                    <form onSubmit={handleSend} className="relative flex items-center">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask about university policies, courses..."
                            className="w-full bg-gray-800 border-none outline-none text-white placeholder-gray-500 rounded-full py-3.5 pl-6 pr-14 focus:ring-2 focus:ring-indigo-500/50 transition-all font-medium"
                            disabled={loading}
                        />
                        <button
                            type="submit"
                            disabled={loading || !input.trim()}
                            className="absolute right-2 p-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:hover:bg-indigo-600 rounded-full transition-colors text-white"
                        >
                            <Send size={18} />
                        </button>
                    </form>
                    <div className="text-center mt-2">
                        <span className="text-xs text-gray-600">Powered by RAG & Gemini</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
