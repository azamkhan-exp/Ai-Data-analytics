import React, { useState, useRef, useEffect } from 'react';
import { askQuestion } from '../api';
import PlotlyChart from './PlotlyChart';
import { Send, Sparkles, User, Bot, RefreshCw, HelpCircle, ArrowRight } from 'lucide-react';

export default function ChatInterface({ datasetId, defaultSuggestions }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: "Hello! I am your AI Data Analyst powered by Python and Pandas. Ask me anything about this dataset—such as key averages, top performers, monthly trends, missing values, or correlations.",
      data: null,
      chart: null,
      suggestions: [
        "What is the average sales?",
        "Which product generated the highest revenue?",
        "Which month had the highest sales?",
        "Are there missing values?",
        "What are the top 10 rows?"
      ]
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (queryText) => {
    const textToSend = queryText || inputQuery;
    if (!textToSend.trim() || loading) return;

    const userMessage = { role: 'user', text: textToSend };
    setMessages((prev) => [...prev, userMessage]);
    setInputQuery('');
    setLoading(true);

    try {
      const response = await askQuestion(datasetId, textToSend);
      const assistantMessage = {
        role: 'assistant',
        text: response.answer,
        data: response.data,
        chart: response.chart,
        suggestions: response.suggestions
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: `Error processing question: ${err.response?.data?.detail || err.message}. Please try rephrasing with specific column names.`,
          data: null,
          chart: null
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xs flex flex-col h-[720px] overflow-hidden transition-colors duration-200">
      {/* Header */}
      <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center shadow-xs">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-800 dark:text-slate-100">Ask Your Data 2.0</h3>
            <p className="text-[11px] text-slate-500 dark:text-slate-400">Natural language questions safely executed via parameterized Pandas operations (zero eval/exec)</p>
          </div>
        </div>

        <button
          onClick={() => setMessages([messages[0]])}
          className="text-xs text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 flex items-center gap-1 transition-colors cursor-pointer"
        >
          <RefreshCw className="w-3 h-3" />
          <span>Reset Chat</span>
        </button>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 p-5 overflow-y-auto space-y-5 bg-slate-50/30 dark:bg-slate-950/50">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'assistant' && (
              <div className="w-7 h-7 rounded-full bg-blue-600 text-white flex items-center justify-center shrink-0 mt-0.5 shadow-xs">
                <Bot className="w-4 h-4" />
              </div>
            )}

            <div
              className={`max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white shadow-xs rounded-tr-xs'
                  : 'bg-white dark:bg-slate-800 border border-slate-200/90 dark:border-slate-700 text-slate-800 dark:text-slate-200 shadow-xs rounded-tl-xs'
              }`}
            >
              {/* Answer text */}
              <div
                className="prose prose-xs dark:prose-invert max-w-none font-sans"
                dangerouslySetInnerHTML={{
                  __html: msg.text
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\n/g, '<br/>')
                }}
              />

              {/* Data Table Result */}
              {msg.data && msg.data.length > 0 && typeof msg.data[0] === 'object' && (
                <div className="mt-3 overflow-x-auto border border-slate-200 dark:border-slate-700 rounded-lg max-h-48">
                  <table className="w-full text-left border-collapse text-[11px]">
                    <thead className="bg-slate-50 dark:bg-slate-700/80 border-b border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-300 sticky top-0">
                      <tr>
                        {Object.keys(msg.data[0]).map((k) => (
                          <th key={k} className="py-1.5 px-2.5 font-semibold capitalize">
                            {k.replace('_', ' ')}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-slate-700 font-mono text-slate-700 dark:text-slate-300">
                      {msg.data.map((row, rIdx) => (
                        <tr key={rIdx} className="hover:bg-slate-50 dark:hover:bg-slate-750">
                          {Object.values(row).map((v, cIdx) => (
                            <td key={cIdx} className="py-1 px-2.5 whitespace-nowrap">
                              {String(v)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {/* Plotly Chart Result */}
              {msg.chart && (
                <div className="mt-4 border border-slate-200 dark:border-slate-700 rounded-xl p-2 bg-white dark:bg-slate-900">
                  <PlotlyChart spec={msg.chart} style={{ height: '300px' }} />
                </div>
              )}

              {/* Suggested Followups */}
              {msg.suggestions && msg.suggestions.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-100 dark:border-slate-700">
                  <div className="text-[10px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1">
                    <HelpCircle className="w-3 h-3 text-blue-500" />
                    <span>Suggested Inquiries</span>
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {msg.suggestions.map((sug, sIdx) => (
                      <button
                        key={sIdx}
                        onClick={() => handleSend(sug)}
                        className="px-2.5 py-1 text-[11px] font-medium bg-slate-50 dark:bg-slate-700/60 border border-slate-200 dark:border-slate-600 hover:border-blue-300 hover:bg-blue-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg transition-all text-left flex items-center gap-1 cursor-pointer"
                      >
                        <span>{sug}</span>
                        <ArrowRight className="w-2.5 h-2.5 text-blue-500 shrink-0" />
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-7 h-7 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 flex items-center justify-center shrink-0 mt-0.5">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 items-center">
            <div className="w-7 h-7 rounded-full bg-blue-600 text-white flex items-center justify-center shrink-0 shadow-xs">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl rounded-tl-xs px-4 py-3 text-xs text-slate-500 dark:text-slate-400 flex items-center gap-2 shadow-xs">
              <span className="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></span>
              <span>Executing safe Pandas analytics operation...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input bar */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Ask a question (e.g. 'What is the average sales?', 'Which month had the highest sales?')..."
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            className="flex-1 px-4 py-2.5 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 disabled:opacity-60"
          />
          <button
            onClick={() => handleSend()}
            disabled={loading || !inputQuery.trim()}
            className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors shadow-xs disabled:opacity-50 cursor-pointer"
          >
            <Send className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Ask</span>
          </button>
        </div>
      </div>
    </div>
  );
}
