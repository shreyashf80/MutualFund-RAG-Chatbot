export default function TypingIndicator() {
  return (
    <div className="flex justify-start w-full gap-3 animate-fade-in-up">
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary/20 to-primary/5 flex-shrink-0 flex items-center justify-center border border-primary/30 mt-1 shadow-[0_0_12px_rgba(6,182,212,0.1)]">
        <span className="material-symbols-outlined text-primary text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>smart_toy</span>
      </div>
      <div className="glass-modal py-3 px-5 rounded-2xl rounded-tl-sm flex gap-1.5 items-center shadow-[0_8px_32px_rgba(0,0,0,0.5)]">
        <div className="w-2 h-2 rounded-full bg-primary typing-dot"></div>
        <div className="w-2 h-2 rounded-full bg-primary typing-dot"></div>
        <div className="w-2 h-2 rounded-full bg-primary typing-dot"></div>
      </div>
    </div>
  );
}
