import { Scheme } from "@/app/page";

interface SidebarProps {
  schemes: Scheme[];
  onNewAnalysis: () => void;
}

export default function Sidebar({ schemes, onNewAnalysis }: SidebarProps) {
  return (
    <aside className="w-[280px] hidden md:flex flex-col glass-panel rounded-none border-r border-white/5 z-30 flex-shrink-0">
      {/* Sidebar Header */}
      <div className="p-5 border-b border-white/5">
        <h2 className="typo-title-md text-on-surface">Supported Schemes</h2>
      </div>
      
      {/* Scheme List */}
      <nav className="flex-1 overflow-y-auto py-3 px-2 flex flex-col gap-0.5">
        {schemes.length === 0 ? (
          <div className="px-4 py-3 typo-body-sm text-on-surface-variant">Loading schemes…</div>
        ) : (
          schemes.map((scheme, idx) => (
            <a 
              key={idx}
              href={scheme.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="group flex items-center gap-3 px-3 py-2.5 rounded-xl text-on-surface-variant hover:text-on-surface hover:bg-white/[0.06] transition-all duration-200 cursor-pointer active:scale-[0.98]"
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
      </nav>

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
