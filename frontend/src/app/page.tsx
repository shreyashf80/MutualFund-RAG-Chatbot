"use client";

import { useState, useEffect, useRef } from "react";
import Sidebar from "@/components/Sidebar";
import MessageBubble, { Message } from "@/components/MessageBubble";
import TypingIndicator from "@/components/TypingIndicator";

export default function Home() {
  const [schemes, setSchemes] = useState<{name: string, url: string}[]>([]);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "bot",
      content: "Hello! I am WealthFact, your AI assistant for HDFC Mutual Funds. I can provide strictly factual information about any of our indexed funds. How can I help you today?"
    }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  useEffect(() => {
    // Fetch indexed schemes on mount
    const fetchSchemes = async () => {
      try {
        const IS_LOCAL = typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
        // If local, hit port 8000. If prod, you can use env var.
        const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || (IS_LOCAL ? 'http://127.0.0.1:8000' : '');
        
        const response = await fetch(`${API_BASE_URL}/api/schemes`);
        if (response.ok) {
          const data = await response.json();
          if (data && data.schemes) {
            setSchemes(data.schemes);
          }
        }
      } catch (error) {
        console.error('Failed to fetch schemes:', error);
      }
    };
    
    fetchSchemes();
  }, []);

  const handleSend = async () => {
    const text = inputValue.trim();
    if (!text) return;

    // Add user message
    setMessages(prev => [...prev, { role: "user", content: text }]);
    setInputValue("");
    setIsTyping(true);

    try {
      const IS_LOCAL = typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || (IS_LOCAL ? 'http://127.0.0.1:8000' : '');
      
      const response = await fetch(`${API_BASE_URL}/api/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text })
      });

      if (!response.ok) throw new Error("API Request Failed");
      
      const data = await response.json();
      
      setMessages(prev => [...prev, {
        role: "bot",
        content: data.answer || "I'm sorry, I couldn't process that request.",
        type: data.type,
        citation: data.citation,
        lastUpdated: data.last_updated
      }]);
      
    } catch (error) {
      setMessages(prev => [...prev, {
        role: "bot",
        content: "Network error: Unable to connect to the WealthFact servers. Please try again later.",
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  const resetChat = () => {
    setMessages([
      {
        role: "bot",
        content: "Hello! I am WealthFact, your AI assistant for HDFC Mutual Funds. I can provide strictly factual information about any of our indexed funds. How can I help you today?"
      }
    ]);
  };

  return (
    <div className="flex h-screen w-full bg-background font-sans overflow-hidden text-on-surface">
      <Sidebar schemes={schemes} onLogoClick={resetChat} />

      <main className="flex-1 flex flex-col h-full relative w-full md:max-w-[calc(100%-20rem)] bg-background">
        {/* Mobile Header */}
        <header className="md:hidden flex items-center justify-between p-4 border-b border-outline/30 bg-surface z-10 shadow-sm">
          <div className="flex items-center gap-3 cursor-pointer" onClick={resetChat}>
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center p-1.5 shrink-0">
              <img src="/logo.svg" alt="Logo" className="w-full h-full object-contain" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-primary tracking-tight leading-tight">WealthFact</h1>
            </div>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto px-4 py-8 md:px-8 custom-scrollbar scroll-smooth">
          {messages.map((msg, i) => (
            <MessageBubble key={i} message={msg} />
          ))}
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} className="h-4" />
        </div>

        {/* Input Area */}
        <div className="p-4 md:p-6 bg-gradient-to-t from-background via-background to-transparent pb-6 md:pb-8">
          <div className="max-w-3xl mx-auto relative group">
            <input 
              type="text" 
              className="w-full bg-surface border border-outline/40 text-on-surface rounded-full pl-6 pr-14 py-4 focus:outline-none focus:border-primary/50 focus:ring-4 focus:ring-primary/10 transition-all shadow-sm placeholder:text-on-surface-variant/50 text-[15px]"
              placeholder="Ask a factual question about HDFC funds..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              autoComplete="off"
            />
            <button 
              onClick={handleSend}
              disabled={!inputValue.trim() || isTyping}
              className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 bg-primary hover:bg-primary-fixed text-on-primary rounded-full flex items-center justify-center transition-all disabled:opacity-50 disabled:hover:bg-primary cursor-pointer active:scale-95"
            >
              <span className="material-symbols-outlined text-[20px] ml-0.5">send</span>
            </button>
          </div>
          <div className="text-center mt-3 flex items-center justify-center gap-1.5 text-xs text-on-surface-variant/60">
            <span className="material-symbols-outlined text-[14px]">info</span>
            <p>WealthFact provides <span className="font-medium text-on-surface-variant/80">factual information only</span> and cannot offer investment advice.</p>
          </div>
        </div>
      </main>
    </div>
  );
}
