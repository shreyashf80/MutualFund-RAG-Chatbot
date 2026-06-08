import { Scheme } from "@/app/page";

interface SidebarProps {
  schemes: Scheme[];
  onNewAnalysis: () => void;
  onSchemeSelect?: (scheme: Scheme) => void;
  onViewChange?: (view: "chat" | "about") => void;
  currentView?: "chat" | "about";
}

export default function Sidebar({ schemes, onNewAnalysis, onSchemeSelect, onViewChange, currentView = "chat" }: SidebarProps) {
  return (
    <aside className="w-[280px] hidden md:flex flex-col glass-panel rounded-none border-r border-white/5 z-30 flex-shrink-0">
      
      {/* Top Action */}
      <div className="p-4 border-b border-white/5">
        <button 
          onClick={onNewAnalysis}
          className="w-full py-2.5 px-5 rounded-full border border-primary/40 text-primary hover:bg-primary/10 hover:border-primary hover:shadow-[0_0_12px_rgba(6,182,212,0.15)] transition-all duration-300 flex items-center justify-center gap-2 typo-label bg-surface/20 active:scale-[0.97]"
        >
          <span className="material-symbols-outlined text-base">add</span>
          New Analysis
        </button>
      </div>

      {/* Sidebar Header */}
      <div className="pt-6 pb-4 px-5 flex items-center gap-2.5 border-b border-white/5">
        <span className="material-symbols-outlined text-primary text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>account_balance</span>
        <h2 className="typo-label text-on-surface-variant">Supported Schemes</h2>
      </div>
      
      {/* Scheme List */}
      <div className="flex-1 overflow-y-auto py-3 px-2 flex flex-col gap-0.5">
        {schemes.length === 0 ? (
          <div className="px-4 py-3 typo-body-sm text-on-surface-variant">Loading schemes…</div>
        ) : (
          schemes.map((scheme, idx) => (
            <a 
              key={idx}
              onClick={(e) => { e.preventDefault(); onViewChange?.("chat"); onSchemeSelect?.(scheme); }}
              className="group flex items-center gap-3 px-3 py-2.5 rounded-xl text-on-surface-variant transition-all duration-200 cursor-pointer active:scale-[0.98]"
            >
              <img 
                src="https://assets-netstorage.groww.in/mf-assets/logos/hdfc_groww.png" 
                alt="" 
                className="w-5 h-5 rounded-full flex-shrink-0 opacity-60 group-hover:opacity-100 transition-opacity" 
              />
              <span className="typo-body-sm font-medium leading-snug transition-all duration-300 group-hover:text-white group-hover:[text-shadow:0_0_4px_rgba(255,255,255,0.25)]">{scheme.name}</span>
            </a>
          ))
        )}
      </div>

      {/* Footer Action (About) */}
      <div className="p-3 border-t border-white/5">
        <a 
          onClick={(e) => { e.preventDefault(); onViewChange?.("about"); }}
          className={`group flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 cursor-pointer active:scale-[0.98] ${currentView === 'about' ? 'bg-primary/10 text-primary font-medium' : 'text-on-surface-variant hover:text-on-surface hover:bg-white/[0.06]'}`}
        >
          <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>info</span>
          <span className="typo-body-sm leading-snug">About</span>
        </a>
      </div>
    </aside>
  );
}
