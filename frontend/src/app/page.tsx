"use client";

import React, { useState, useEffect, useRef } from "react";
import Sidebar from "@/components/Sidebar";
import MessageBubble from "@/components/MessageBubble";
import TypingIndicator from "@/components/TypingIndicator";
import About from "@/components/About";

export interface Scheme {
  name: string;
  url: string;
}

export interface Message {
  role: "user" | "bot";
  content: string;
  type?: string;
  citation?: string;
  lastUpdated?: string;
  options?: { label: string, query: string }[];
}

export default function Home() {
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [currentView, setCurrentView] = useState<"chat" | "about">("chat");
  const [selectedScheme, setSelectedScheme] = useState<Scheme | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const showWelcome = messages.length === 0;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  useEffect(() => {
    const fetchSchemes = async () => {
      try {
        const response = await fetch('/api/schemes');
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

  const handleQuery = async (text: string) => {
    if (!text.trim() || isTyping) return;

    setMessages(prev => [...prev, { role: "user", content: text }]);
    setInputValue("");
    setIsTyping(true);

    try {
      const body: { query: string; scheme_name?: string } = { query: text };
      // Always scope retrieval to the active scheme so vague questions like
      // "what is NAV" or "who is fund manager" return data for the correct fund.
      if (selectedScheme) {
        body.scheme_name = selectedScheme.name;
      }

      const response = await fetch('/api/query', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      if (!response.ok) throw new Error("API Request Failed");
      
      const data = await response.json();
      
      setMessages(prev => [...prev, {
        role: "bot",
        content: data.answer || "I'm sorry, I couldn't process that request.",
        type: data.type,
        citation: data.citation || data.educational_link,
        lastUpdated: data.last_updated
      }]);
      
    } catch {
      setMessages(prev => [...prev, {
        role: "bot",
        content: "Network error: Unable to connect to the WealthFact servers. Please try again later.",
        type: 'refusal'
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSend = () => {
    handleQuery(inputValue);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  const resetChat = (e?: React.MouseEvent) => {
    if (e) e.preventDefault();
    setMessages([]);
    setInputValue('');
    setCurrentView("chat");
    setSelectedScheme(null); // Clear scheme context on reset
  };

  const handleSchemeSelect = (scheme: Scheme) => {
    setSelectedScheme(scheme); // Set active scheme context for scoped retrieval
    setMessages([{
      role: "bot",
      content: `What would you like to know about ${scheme.name}?`,
      options: [
        { label: "NAV", query: `What is the NAV of ${scheme.name}?` },
        { label: "AUM", query: `What is the AUM of ${scheme.name}?` },
        { label: "Fund Manager", query: `Who is the fund manager of ${scheme.name}?` },
        { label: "Expense Ratio", query: `What is the expense ratio of ${scheme.name}?` }
      ]
    }]);
    setInputValue('');
  };

  const questionTemplates = [
    (name: string) => `What is the expense ratio of ${name}?`,
    (name: string) => `What is the exit load for ${name}?`,
    (name: string) => `Who is the fund manager of ${name}?`,
    (name: string) => `What is the NAV of ${name}?`,
    (name: string) => `What is the minimum investment for ${name}?`,
    (name: string) => `What is the AUM of ${name}?`,
  ];

  const exampleQuestions = React.useMemo(() => {
    if (schemes.length === 0) {
      return [
        "What is the expense ratio of HDFC Top 100?",
        "What is the exit load for HDFC Defence Fund?",
        "Who is the fund manager of HDFC Flexi Cap?"
      ];
    }
    const shuffled = [...schemes].sort(() => Math.random() - 0.5);
    const picked = shuffled.slice(0, 3);
    const shuffledTemplates = [...questionTemplates].sort(() => Math.random() - 0.5);
    return picked.map((scheme, i) => shuffledTemplates[i](scheme.name));
  }, [schemes]);

  return (
    <div className="h-screen w-full overflow-hidden flex flex-col typo-body antialiased">
      
      {/* ─── Top Navigation Bar ────────────────────────────────────────── */}
      <nav className="w-full z-40 glass-panel flex justify-between items-center px-6 py-4 rounded-none border-b border-white/5 flex-shrink-0">
        <div className="flex items-center gap-3">
          <button className="md:hidden text-primary p-2 hover:bg-white/5 rounded-full transition-colors" aria-label="Menu">
            <span className="material-symbols-outlined">menu</span>
          </button>
          <a onClick={resetChat} className="flex items-center gap-1.5 md:gap-2.5 cursor-pointer select-none">
            <img src="/logo.svg" alt="WealthFact Logo" className="w-10 h-10 md:w-12 md:h-12" />
            <div className="flex flex-col md:flex-row md:items-baseline md:gap-3">
              <h1 className="text-2xl md:text-[32px] font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary-fixed leading-tight">
                WealthFact
              </h1>
              <span className="text-on-surface-variant/60 text-[13px] md:text-sm font-normal tracking-wider mt-0.5 md:mt-0">
                Instant facts, zero fiction
              </span>
            </div>
          </a>
        </div>
      </nav>

      <div className="flex-1 flex w-full overflow-hidden relative">
        {/* ─── Sidebar ─────────────────────────────────────────────────── */}
        <Sidebar 
          schemes={schemes} 
          onNewAnalysis={resetChat} 
          onSchemeSelect={handleSchemeSelect} 
          onViewChange={setCurrentView}
          currentView={currentView}
        />

        {/* ─── Main Content ────────────────────────────────────────────── */}
        <main className="flex-1 relative flex flex-col h-full overflow-hidden mb-[64px] md:mb-0">
          
          {currentView === "about" ? (
            <About />
          ) : (
            <>
              {/* Disclaimer Banner */}
              <div className={`absolute top-0 left-0 w-full z-30 flex justify-center py-3 pointer-events-none transition-opacity duration-300 ${showWelcome ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
                <div className="glass-modal pointer-events-auto flex items-center gap-2 py-1.5 px-4 rounded-full border border-tertiary/20 shadow-[0_0_20px_rgba(245,158,11,0.1)]">
                  <span className="material-symbols-outlined text-tertiary text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>warning</span>
                  <span className="text-tertiary typo-label">Facts-only · No investment advice</span>
                </div>
              </div>

              {/* ─── Chat Area ───────────────────────────────────────────── */}
              <div className="flex-1 overflow-y-auto p-4 md:p-6 flex flex-col pt-14">
                
                {showWelcome ? (
                  /* ─── Welcome State ─────────────────────────────────────── */
                  <div className="flex flex-col items-center justify-center h-full text-center w-full mx-auto animate-fade-in-up">
                    <div className="w-20 h-20 rounded-full bg-gradient-to-br from-primary/20 to-transparent flex items-center justify-center mb-8 border border-primary/30 shadow-[0_0_40px_rgba(6,182,212,0.15)] relative">
                      <div className="absolute inset-0 rounded-full bg-primary/10 blur-xl"></div>
                      <span className="material-symbols-outlined text-primary text-4xl relative z-10" style={{ fontVariationSettings: "'FILL' 1" }}>analytics</span>
                    </div>
                    <h2 className="text-3xl md:text-4xl font-bold text-on-surface mb-4 leading-tight tracking-tight">
                      How can I assist your analysis today?
                    </h2>
                    <p className="text-on-surface-variant typo-body mb-10 max-w-xl">
                      Ask questions about mutual fund metrics, performance history, or regulatory details.
                    </p>
                    <div className="flex flex-wrap justify-center gap-3">
                      {exampleQuestions.map((q, idx) => (
                        <button 
                          key={idx}
                          onClick={() => handleQuery(q)}
                          className="px-5 py-2.5 rounded-full border border-primary/20 text-primary typo-body-sm hover:bg-primary/10 hover:border-primary/50 transition-all duration-300 glass-modal shadow-lg hover:shadow-[0_0_15px_rgba(6,182,212,0.15)]"
                        >
                          {q}
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  /* ─── Chat Messages ─────────────────────────────────────── */
                  <div className="flex flex-col gap-6 w-full">
                    {messages.map((msg, idx) => (
                      <div key={idx} className="flex flex-col gap-2">
                        <MessageBubble message={msg} />
                        {msg.options && (
                          <div className="flex flex-wrap gap-2 mt-1 ml-0 md:ml-[52px]">
                            {msg.options.map((opt, oIdx) => (
                              <button
                                key={oIdx}
                                onClick={() => handleQuery(opt.query)}
                                disabled={isTyping}
                                className="px-4 py-1.5 rounded-full border border-primary/20 text-primary text-sm hover:bg-primary/10 hover:border-primary/50 transition-all duration-300 glass-modal shadow-sm disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
                              >
                                {opt.label}
                              </button>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                    {isTyping && <TypingIndicator />}
                    <div ref={messagesEndRef} className="h-28 w-full flex-shrink-0" />
                  </div>
                )}
                
              </div>

              {/* ─── Floating Input Bar ──────────────────────────────────── */}
              <div className="absolute bottom-0 left-0 w-full p-4 md:p-6 bg-gradient-to-t from-background via-background/90 to-transparent pointer-events-none flex justify-center z-20">
                <div className="w-full pointer-events-auto relative">
                  <div className="glass-modal rounded-full flex items-center p-1.5 pl-6 pr-1.5 shadow-[0_8px_32px_rgba(0,0,0,0.5)] transition-all duration-300 focus-within:border-primary/40 focus-within:shadow-[0_0_20px_rgba(6,182,212,0.12)]">
                    <input 
                      className="flex-1 bg-transparent border-none outline-none text-on-surface placeholder:text-on-surface-variant/40 typo-body focus:ring-0" 
                      placeholder="Ask about a scheme..." 
                      type="text"
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      onKeyDown={handleKeyDown}
                    />
                    <button 
                      onClick={handleSend}
                      disabled={!inputValue.trim() || isTyping}
                      className="w-10 h-10 rounded-full bg-gradient-to-r from-primary to-primary-fixed text-on-primary flex items-center justify-center hover:shadow-[0_0_15px_rgba(34,211,238,0.5)] transition-all duration-300 ml-2 disabled:opacity-40 disabled:cursor-not-allowed active:scale-95"
                      aria-label="Send message"
                    >
                      <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>send</span>
                    </button>
                  </div>
                  {/* Footer Links */}
                  <div className="hidden md:flex justify-center items-center gap-4 mt-3 opacity-40">
                    <a className="typo-label text-on-surface-variant hover:text-primary transition-colors" href="#">Terms of Service</a>
                    <span className="w-1 h-1 rounded-full bg-on-surface-variant/50"></span>
                    <a className="typo-label text-on-surface-variant hover:text-primary transition-colors" href="#">Data Privacy</a>
                  </div>
                </div>
              </div>
            </>
          )}

        </main>
      </div>

      {/* ─── Mobile Bottom Nav ───────────────────────────────────────── */}
      <nav className="fixed bottom-0 left-0 w-full md:hidden glass-panel border-t border-white/5 rounded-none z-50 flex justify-around items-center h-[64px]">
        <a className="flex flex-col items-center justify-center w-full h-full text-primary" href="#">
          <span className="material-symbols-outlined mb-0.5" style={{ fontVariationSettings: "'FILL' 1" }}>explore</span>
          <span className="text-[10px] font-medium tracking-wide">Explore</span>
        </a>
      </nav>

    </div>
  );
}
