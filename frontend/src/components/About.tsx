import React from 'react';

export default function About() {
  return (
    <div className="w-full h-full overflow-y-auto p-6 md:p-12 animate-fade-in-up">
      <div className="max-w-4xl mx-auto glass-modal rounded-3xl p-8 md:p-12 border border-white/5 shadow-2xl">
        <div className="flex items-center gap-4 mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center border border-primary/20">
            <span className="material-symbols-outlined text-3xl text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>info</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-on-surface tracking-tight">About WealthFact</h1>
            <p className="text-primary mt-1 font-medium">Instant facts, zero fiction.</p>
          </div>
        </div>

        <div className="space-y-8 text-on-surface-variant typo-body leading-relaxed">
          <section>
            <h2 className="text-xl font-semibold text-on-surface mb-3 flex items-center gap-2">
              <span className="material-symbols-outlined text-tertiary text-sm">target</span>
              Project Scope
            </h2>
            <p>
              WealthFact is a specialized AI assistant designed exclusively to answer factual queries about HDFC Mutual Fund schemes available on Groww. It utilizes a Retrieval-Augmented Generation (RAG) architecture to ensure that every answer is strictly grounded in officially scraped data.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-on-surface mb-3 flex items-center gap-2">
              <span className="material-symbols-outlined text-tertiary text-sm">verified</span>
              What's Included
            </h2>
            <ul className="list-none space-y-3">
              <li className="flex items-start gap-3">
                <span className="material-symbols-outlined text-primary mt-0.5 text-[18px]">check_circle</span>
                <span><strong>Key Metrics:</strong> Latest NAV, AUM (Fund Size), Expense Ratios, and Minimum SIP amounts.</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="material-symbols-outlined text-primary mt-0.5 text-[18px]">check_circle</span>
                <span><strong>Fund Management:</strong> Details about current fund managers, their tenure, and educational background.</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="material-symbols-outlined text-primary mt-0.5 text-[18px]">check_circle</span>
                <span><strong>Policies:</strong> Exit loads, stamp duty, tax implications, and lock-in periods.</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="material-symbols-outlined text-primary mt-0.5 text-[18px]">check_circle</span>
                <span><strong>Objectives:</strong> Investment objectives and benchmark indices.</span>
              </li>
            </ul>
          </section>

          <section className="bg-tertiary/10 border border-tertiary/20 rounded-2xl p-6 mt-8">
            <h2 className="text-lg font-semibold text-tertiary mb-2 flex items-center gap-2">
              <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>warning</span>
              Important Limitations
            </h2>
            <p className="text-sm">
              This assistant is strictly factual. It will <strong>never</strong> provide investment advice, predict future returns, compare funds against each other, or offer opinions. If the information is not explicitly found in the source documents, the AI will refuse to answer rather than hallucinate.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
