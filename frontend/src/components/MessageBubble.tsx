export interface Message {
  role: "user" | "bot";
  content: string;
  type?: string;
  citation?: string;
  lastUpdated?: string;
}

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex w-full max-w-3xl mx-auto mb-6 slide-up fade-in ${isUser ? 'justify-end pl-12' : 'justify-start pr-12'}`}>
      
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-surface-bright flex items-center justify-center shrink-0 mt-1 border border-primary/20 shadow-lg shadow-primary/5">
          <span className="material-symbols-outlined text-[18px] text-primary">robot_2</span>
        </div>
      )}

      <div 
        className={`relative ${isUser ? 'mr-0 ml-4 max-w-[85%]' : 'ml-4 mr-0 max-w-[85%]'} 
          ${isUser ? 'bg-primary text-on-primary' : 'bg-surface border border-outline/30 text-on-surface'} 
          rounded-2xl px-5 py-4 shadow-sm leading-relaxed text-[15px]
          ${isUser ? 'rounded-tr-none' : 'rounded-tl-none'}
        `}
      >
        <div className="whitespace-pre-wrap">{message.content}</div>
        
        {message.citation && (
          <div className="mt-4 pt-3 border-t border-outline/20">
            <div className="flex flex-col gap-1.5 text-xs">
              <a 
                href={message.citation} 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-primary hover:text-primary-fixed hover:underline transition-colors w-fit group"
              >
                <span className="material-symbols-outlined text-[14px]">link</span>
                <span className="font-medium group-hover:underline">{message.citation}</span>
              </a>
              {message.lastUpdated && (
                <div className="flex items-center gap-1.5 text-on-surface-variant/70">
                  <span className="material-symbols-outlined text-[14px]">update</span>
                  <span>Data from: {message.lastUpdated}</span>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center shrink-0 mt-1 ml-4 border border-primary/30">
          <span className="material-symbols-outlined text-[18px] text-primary">person</span>
        </div>
      )}
    </div>
  );
}
