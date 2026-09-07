import React, { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';

export default function PlotlyChart({ spec, style, className }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current || !spec) return;

    const data = spec.data || [];
    const layout = {
      autosize: true,
      responsive: true,
      margin: { l: 50, r: 30, t: 50, b: 50 },
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      font: { family: 'system-ui, -apple-system, sans-serif', color: '#475569', size: 12 },
      ...(spec.layout || {}),
    };

    const config = {
      responsive: true,
      displayModeBar: true,
      displaylogo: false,
      modeBarButtonsToRemove: ['lasso2d', 'select2d'],
      toImageButtonOptions: {
        format: 'png',
        filename: 'data_chart',
        height: 600,
        width: 900,
        scale: 2,
      },
      ...(spec.config || {}),
    };

    Plotly.react(containerRef.current, data, layout, config);

    const handleResize = () => {
      if (containerRef.current) {
        Plotly.Plots.resize(containerRef.current);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [spec]);

  if (!spec) {
    return (
      <div className="flex items-center justify-center p-8 bg-slate-50 border border-slate-200 rounded-lg text-slate-400 text-sm">
        No chart specification available
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      style={{ width: '100%', height: '100%', minHeight: '340px', ...style }}
      className={`w-full overflow-hidden ${className || ''}`}
    />
  );
}
