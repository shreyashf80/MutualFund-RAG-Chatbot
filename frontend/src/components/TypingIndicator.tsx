export default function TypingIndicator() {
  return (
    <div className="flex w-full max-w-3xl mx-auto mb-6 slide-up fade-in justify-start">
      <div className="w-8 h-8 rounded-full bg-surface-bright flex items-center justify-center shrink-0 mt-1 border border-primary/20 shadow-lg shadow-primary/5">
        <span className="material-symbols-outlined text-[18px] text-primary">robot_2</span>
      </div>
      <div className="ml-4 max-w-[85%] bg-surface border border-outline/30 rounded-2xl rounded-tl-none px-5 py-4">
        <div className="flex items-center gap-1.5 h-5">
          <div className="w-2 h-2 rounded-full bg-primary/60 animate-typing-bounce"></div>
          <div className="w-2 h-2 rounded-full bg-primary/60 animate-typing-bounce animation-delay-100"></div>
          <div className="w-2 h-2 rounded-full bg-primary/60 animate-typing-bounce animation-delay-200"></div>
        </div>
      </div>
    </div>
  );
}
