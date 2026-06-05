import { Message } from "@/app/page";

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end w-full animate-fade-in-up">
        <div className="max-w-[85%] md:max-w-[70%] bg-gradient-to-br from-primary-container to-primary text-on-primary typo-body p-4 rounded-2xl rounded-tr-sm shadow-[0_8px_30px_rgba(6,182,212,0.25),0_2px_8px_rgba(0,0,0,0.4)]">
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>
      </div>
    );
  }

  const isRefusal = message.type === 'refusal';

  return (
    <div className="flex justify-start w-full gap-3 animate-fade-in-up">
      {/* Bot Avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary/20 to-primary/5 flex-shrink-0 flex items-center justify-center border border-primary/30 mt-1 shadow-[0_0_12px_rgba(6,182,212,0.1)]">
        <span className="material-symbols-outlined text-primary text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>smart_toy</span>
      </div>
      
      {/* Bot Message Body */}
      <div className={`max-w-[85%] md:max-w-[75%] glass-modal p-5 rounded-2xl rounded-tl-sm shadow-[0_8px_32px_rgba(0,0,0,0.5),0_0_0_1px_rgba(255,255,255,0.03)] ${isRefusal ? 'border-error/30 shadow-[inset_4px_0_0_rgba(239,68,68,0.5)]' : ''}`}>
        {isRefusal ? (
          <>
            <div className="flex items-center gap-2 mb-3">
              <span className="px-2 py-0.5 bg-error/10 text-error typo-label rounded">Notice</span>
            </div>
            <p className="text-on-surface leading-relaxed whitespace-pre-wrap typo-body">{message.content}</p>
            {message.citation && (
              <a href={message.citation} target="_blank" rel="noopener noreferrer" className="inline-flex mt-4 px-4 py-2 bg-error-container/30 border border-error/20 text-error hover:bg-error-container/50 transition-colors rounded-lg typo-body-sm items-center gap-2 font-medium">
                <span className="material-symbols-outlined text-sm">school</span> Investor Knowledge Center ↗
              </a>
            )}
          </>
        ) : (
          <>
            <p className="text-on-surface leading-relaxed typo-body whitespace-pre-wrap">{message.content}</p>
            
            {(message.citation || message.lastUpdated) && (
              <div className="flex flex-wrap items-center justify-between gap-2 mt-4 pt-3 border-t border-white/5">
                {message.citation ? (
                  <a className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-surface-bright/50 hover:bg-surface-bright transition-colors rounded-lg typo-label text-on-surface-variant hover:text-on-surface border border-white/5" target="_blank" rel="noopener noreferrer" href={message.citation}>
                    <span className="material-symbols-outlined text-[14px]">link</span>
                    Source Link ↗
                  </a>
                ) : <div></div>}
                
                {message.lastUpdated && (
                  <span className="text-[11px] text-on-surface-variant/40 font-medium tracking-wide">
                    Updated: {message.lastUpdated}
                  </span>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
