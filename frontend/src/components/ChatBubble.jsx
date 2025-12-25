import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot } from 'lucide-react';

const ChatBubble = ({ message }) => {
    const isUser = message.sender === 'user';

    return (
        <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
            <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-2`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${isUser ? 'bg-indigo-600' : 'bg-emerald-600'}`}>
                    {isUser ? <User size={16} className="text-white" /> : <Bot size={16} className="text-white" />}
                </div>

                <div className={`p-4 rounded-2xl ${isUser ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-gray-700 text-gray-100 rounded-tl-none'} shadow-md`}>
                    <div className="markdown-body text-sm leading-relaxed">
                        {isUser ? message.text : <ReactMarkdown>{message.text}</ReactMarkdown>}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatBubble;
