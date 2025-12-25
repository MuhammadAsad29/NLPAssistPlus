import React from 'react';
import { BookOpen } from 'lucide-react';

const SourceList = ({ sources }) => {
    if (!sources || sources.length === 0) return null;

    return (
        <div className="mt-2 text-xs text-gray-400 pl-12">
            <div className="flex items-center gap-1 mb-1 font-semibold">
                <BookOpen size={12} />
                <span>Sources:</span>
            </div>
            <div className="flex flex-wrap gap-2">
                {sources.map((source, idx) => (
                    <span key={idx} className="bg-gray-800 border border-gray-700 px-2 py-0.5 rounded text-gray-300">
                        {source}
                    </span>
                ))}
            </div>
        </div>
    );
};

export default SourceList;
