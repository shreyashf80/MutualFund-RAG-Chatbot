import { useState } from "react";
import { Scheme } from "@/app/page";

interface SidebarProps {
  schemes: Scheme[];
  onNewAnalysis: () => void;
  onSchemeSelect?: (scheme: Scheme) => void;
  onViewChange?: (view: "chat" | "about") => void;
  currentView?: "chat" | "about";
}

export default function Sidebar({ schemes, onNewAnalysis, onSchemeSelect, onViewChange, currentView = "chat" }: SidebarProps) {
  const [isSchemesOpen, setIsSchemesOpen] = useState(true);
  return (
    <aside className="w-[280px] hidden md:flex flex-col glass-panel rounded-none border-r border-white/5 z-30 flex-shrink-0">
      <div className="flex-1 overflow-y-auto py-4 px-2 flex flex-col gap-1">
        
        {/* About Link */}
        <a 
          onClick={(e) => { e.preventDefault(); onViewChange?.("about"); }}
          className={`group flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200 cursor-pointer active:scale-[0.98] ${currentView === 'about' ? 'bg-primary/10 text-primary font-medium' : 'text-on-surface-variant hover:text-on-surface hover:bg-white/[0.06]'}`}
        >
          <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>info</span>
          <span className="typo-body-sm leading-snug">About Project</span>
        </a>

        <div className="h-px w-full bg-white/5 my-2"></div>

        {/* Sidebar Header / Dropdown Toggle */}
        <button 
          onClick={() => setIsSchemesOpen(!isSchemesOpen)}
          className="flex items-center justify-between w-full px-3 py-2.5 rounded-xl hover:bg-white/[0.04] transition-colors cursor-pointer group"
        >
          <div className="flex items-center gap-2.5">
            <span className="material-symbols-outlined text-primary text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>account_balance</span>
            <h2 className="typo-label text-on-surface-variant group-hover:text-on-surface transition-colors">Supported Schemes</h2>
          </div>
          <span className={`material-symbols-outlined text-on-surface-variant text-sm transition-transform duration-300 ${isSchemesOpen ? 'rotate-180' : ''}`}>expand_more</span>
        </button>
        
        {/* Scheme List */}
        <div className={`flex flex-col gap-0.5 overflow-hidden transition-all duration-300 ${isSchemesOpen ? 'max-h-[1000px] opacity-100 mt-1' : 'max-h-0 opacity-0'}`}>
          {schemes.length === 0 ? (
            <div className="px-4 py-3 typo-body-sm text-on-surface-variant">Loading schemes…</div>
          ) : (
            schemes.map((scheme, idx) => (
              <a 
                key={idx}
                onClick={(e) => { e.preventDefault(); onViewChange?.("chat"); onSchemeSelect?.(scheme); }}
                className="group flex items-center gap-3 px-3 py-2.5 rounded-xl text-on-surface-variant hover:text-on-surface hover:bg-white/[0.06] transition-all duration-200 cursor-pointer active:scale-[0.98] ml-2"
              >
                <img 
                  src="https://assets-netstorage.groww.in/mf-assets/logos/hdfc_groww.png" 
                  alt="" 
                  className="w-5 h-5 rounded-full flex-shrink-0 opacity-60 group-hover:opacity-100 transition-opacity" 
                />
                <span className="typo-body-sm font-medium leading-snug">{scheme.name}</span>
              </a>
            ))
          )}
        </div>
      </div>

      {/* Footer Action */}
      <div className="p-4 border-t border-white/5">
        <button 
          onClick={onNewAnalysis}
          className="w-full py-2.5 px-5 rounded-full border border-primary/40 text-primary hover:bg-primary/10 hover:border-primary hover:shadow-[0_0_12px_rgba(6,182,212,0.15)] transition-all duration-300 flex items-center justify-center gap-2 typo-label bg-surface/20 active:scale-[0.97]"
        >
          <span className="material-symbols-outlined text-base">add</span>
          New Analysis
        </button>
      </div>
    </aside>
  );
}
