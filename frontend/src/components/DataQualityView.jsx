import React from 'react';
import { ShieldCheck, AlertTriangle, CheckCircle2, Wrench, ArrowRight } from 'lucide-react';

export default function DataQualityView({ qualityScore = {}, onOpenCleaner }) {
  const { 
    score = 100, 
    rating = 'Good Quality', 
    issues = [], 
    recommendations = [] 
  } = qualityScore;

  const getScoreColor = () => {
    if (score >= 90) return 'text-emerald-600 dark:text-emerald-400 border-emerald-500 bg-emerald-50 dark:bg-emerald-950/40';
    if (score >= 75) return 'text-blue-600 dark:text-blue-400 border-blue-500 bg-blue-50 dark:bg-blue-950/40';
    if (score >= 50) return 'text-amber-600 dark:text-amber-400 border-amber-500 bg-amber-50 dark:bg-amber-950/40';
    return 'text-rose-600 dark:text-rose-400 border-rose-500 bg-rose-50 dark:bg-rose-950/40';
  };

  return (
    <div className="space-y-6">
      {/* Top Hero Score Card */}
      <div className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-xs flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2 text-center md:text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-400 border border-blue-200/60 dark:border-blue-800/60">
            <ShieldCheck className="w-3.5 h-3.5" />
            Automated Dataset Health Audit
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 dark:text-slate-100">
            Data Quality Score
          </h2>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-lg leading-relaxed">
            Evaluated on row completeness, duplicate rates, column variance, outlier bounds, and cardinality entropy.
          </p>
        </div>

        {/* Circular Score Badge */}
        <div className="flex flex-col items-center justify-center shrink-0">
          <div className={`w-28 h-28 sm:w-32 sm:h-32 rounded-full border-4 flex flex-col items-center justify-center shadow-inner ${getScoreColor()}`}>
            <span className="text-3xl sm:text-4xl font-extrabold font-mono tracking-tight">{score}</span>
            <span className="text-[11px] font-bold uppercase tracking-wider opacity-80">/ 100</span>
          </div>
          <span className="mt-2 text-xs font-extrabold uppercase tracking-wider text-slate-700 dark:text-slate-300">
            {rating}
          </span>
        </div>
      </div>

      {/* Hygiene Issues & Penalties */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 rounded-3xl shadow-xs p-6 space-y-4">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-500" />
          <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">
            Diagnostic Factor Penalties
          </h3>
        </div>

        {issues.length === 0 ? (
          <div className="p-6 text-center text-emerald-600 dark:text-emerald-400 flex flex-col items-center gap-1.5">
            <CheckCircle2 className="w-6 h-6" />
            <span className="font-bold text-xs">Zero hygiene deductions applied! 100% complete dataset.</span>
          </div>
        ) : (
          <div className="space-y-2.5">
            {issues.map((iss, i) => (
              <div
                key={i}
                className="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 flex items-start justify-between gap-4"
              >
                <div>
                  <div className="font-bold text-slate-800 dark:text-slate-200 text-xs">{iss.title}</div>
                  <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">{iss.description}</div>
                </div>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-rose-100 dark:bg-rose-950/60 text-rose-700 dark:text-rose-400 border border-rose-200 dark:border-rose-800 shrink-0">
                  {iss.deduction}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recommendations & Remediation */}
      <div className="p-6 rounded-3xl bg-blue-50/70 dark:bg-blue-950/30 border border-blue-200/80 dark:border-blue-800/80 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <h4 className="text-xs font-bold uppercase tracking-wider text-blue-900 dark:text-blue-300">
            Actionable Data Hygiene Recommendations
          </h4>
          <ul className="text-xs text-blue-800 dark:text-blue-300/80 space-y-1 pt-1">
            {recommendations.map((rec, rIdx) => (
              <li key={rIdx} className="flex items-start gap-1.5">
                <span className="font-bold text-blue-600 dark:text-blue-400">•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>

        {onOpenCleaner && (
          <button
            onClick={onOpenCleaner}
            className="flex items-center gap-1.5 px-4 py-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all shadow-xs shrink-0 cursor-pointer"
          >
            <Wrench className="w-3.5 h-3.5" />
            <span>Launch Cleaner</span>
            <ArrowRight className="w-3.5 h-3.5 ml-0.5" />
          </button>
        )}
      </div>
    </div>
  );
}
