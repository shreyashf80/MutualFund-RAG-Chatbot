interface Scheme {
  name: string;
  url: string;
}

interface SidebarProps {
  schemes: Scheme[];
  onLogoClick: () => void;
}

export default function Sidebar({ schemes, onLogoClick }: SidebarProps) {
  return (
    <nav className="w-80 bg-surface border-r border-outline/30 flex flex-col hidden md:flex transition-all duration-300 relative z-20">
      <div 
        className="p-md border-b border-outline/30 flex items-center gap-sm cursor-pointer hover:bg-surface-bright/50 transition-colors duration-200"
        onClick={onLogoClick}
      >
        <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center p-1.5 shrink-0">
          <img src="/logo.svg" alt="WealthFact Logo" className="w-full h-full object-contain" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-primary tracking-tight">WealthFact</h1>
          <p className="text-xs text-on-surface-variant/70 font-medium tracking-wide">HDFC MUTUAL FUND</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-md custom-scrollbar">
        <h2 className="text-sm font-semibold text-on-surface-variant mb-4 uppercase tracking-wider flex items-center gap-2">
          <span className="material-symbols-outlined text-[18px]">inventory_2</span>
          Indexed Schemes
        </h2>
        
        {schemes.length === 0 ? (
          <div className="text-sm text-on-surface-variant/50 flex items-center gap-2 italic">
            <span className="w-4 h-4 rounded-full border-2 border-primary/30 border-t-primary animate-spin"></span>
            Loading schemes...
          </div>
        ) : (
          <ul className="space-y-1">
            {schemes.map((scheme, idx) => (
              <li key={idx}>
                <a 
                  href={scheme.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-start gap-2 p-2 rounded-lg text-sm text-on-surface-variant hover:text-on-surface hover:bg-surface-bright transition-all duration-200 group"
                  title={scheme.name}
                >
                  <span className="material-symbols-outlined text-[16px] mt-0.5 text-primary/50 group-hover:text-primary transition-colors">feed</span>
                  <span className="line-clamp-2 leading-snug">{scheme.name}</span>
                </a>
              </li>
            ))}
          </ul>
        )}
      </div>

      <a 
        href="https://github.com/shreyashf80/MutualFund-RAG-Chatbot" 
        target="_blank" 
        rel="noopener noreferrer"
        className="p-4 border-t border-outline/30 flex items-center gap-3 text-on-surface-variant hover:text-on-surface hover:bg-surface-bright transition-all duration-200"
      >
        <div className="w-8 h-8 rounded-full bg-surface-bright flex items-center justify-center shrink-0 border border-outline/30">
          <span className="material-symbols-outlined text-[18px]">code</span>
        </div>
        <div className="flex flex-col">
          <span className="text-sm font-medium">View Source</span>
          <span className="text-xs text-on-surface-variant/60">Powered by NextLeap</span>
        </div>
      </a>
    </nav>
  );
}
