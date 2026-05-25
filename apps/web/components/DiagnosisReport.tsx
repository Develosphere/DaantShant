"use client";

import type { PipelineResult } from "@/lib/types";

type Props = {
  result: PipelineResult | null;
  label?: string;
  loading?: boolean;
  liveActive?: boolean;
};

function severityClass(severity: string): string {
  const s = severity.toLowerCase();
  if (s === "critical" || s === "high") return "severity-high";
  if (s === "moderate") return "severity-moderate";
  if (s === "mild") return "severity-mild";
  return "severity-none";
}

function conditionIcon(label: string): string {
  const l = label.toLowerCase();
  if (l.includes("healthy")) return "✦";
  if (l.includes("cavity")) return "◉";
  if (l.includes("plaque") || l.includes("tartar")) return "◎";
  if (l.includes("gingivitis") || l.includes("gum")) return "▲";
  if (l.includes("discolor")) return "◐";
  return "?";
}

function formatAction(action: string): string {
  return action.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatLabel(label: string): string {
  return label.replace(/_/g, " ");
}

export function DiagnosisReport({
  result,
  label = "AI Diagnosis",
  loading,
  liveActive,
}: Props) {
  if (loading) {
    return (
      <aside className="report-panel report-panel--loading">
        <div className="report-header">
          <h2>{label}</h2>
          <span className="chip chip-analyzing">Analyzing</span>
        </div>
        <div className="loader-ring">
          <div className="loader-ring-inner" />
        </div>
        <p className="loader-text">Running vision model & clinical mapping…</p>
      </aside>
    );
  }

  if (!result) {
    return (
      <aside className="report-panel report-panel--empty">
        <div className="report-header">
          <h2>{label}</h2>
        </div>
        <div className="empty-illustration">
          <div className="empty-icon">🦷</div>
          <p className="empty-title">Your report appears here</p>
          <p className="empty-desc">
            Start the camera, upload a photo, or run live analysis. Results
            update in real time.
          </p>
        </div>
        <ul className="empty-steps">
          <li><span>1</span> Camera or upload</li>
          <li><span>2</span> Align teeth in frame</li>
          <li><span>3</span> Analyze</li>
        </ul>
      </aside>
    );
  }

  const { analysis, diagnosis } = result;
  const confidencePct = Math.round(diagnosis.confidence * 100);
  const sevClass = severityClass(diagnosis.severity);

  return (
    <aside className={`report-panel report-panel--ready ${liveActive ? "report-panel--live" : ""}`}>
      <div className="report-header">
        <h2>{label}</h2>
        {liveActive && (
          <span className="chip chip-live">
            <span className="live-dot" /> Live
          </span>
        )}
      </div>

      <div className={`condition-hero ${sevClass}`}>
        <div className="condition-icon">{conditionIcon(diagnosis.condition_label)}</div>
        <div className="condition-body">
          <span className="condition-label">Detected condition</span>
          <h3 className="condition-name">{diagnosis.condition_label}</h3>
          <span className={`severity-badge ${sevClass}`}>{diagnosis.severity}</span>
        </div>
        <div className="confidence-ring" style={{ "--pct": confidencePct } as React.CSSProperties}>
          <svg viewBox="0 0 36 36">
            <path
              className="ring-bg"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path
              className="ring-fill"
              strokeDasharray={`${confidencePct}, 100`}
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
          </svg>
          <span className="ring-value">{confidencePct}%</span>
        </div>
      </div>

      <div className="stat-cards">
        <div className="stat-card stat-card-wide">
          <span className="stat-label">Recommended action</span>
          <span className="stat-action">{formatAction(diagnosis.action_trigger)}</span>
        </div>
      </div>

      {analysis.findings.length > 0 && (
        <div className="findings-block">
          <h4>Visual findings</h4>
          <div className="finding-chips">
            {analysis.findings.map((f, i) => (
              <div key={i} className="finding-chip">
                <span className="finding-name">{formatLabel(f.label)}</span>
                <div className="finding-bar-wrap">
                  <div
                    className="finding-bar"
                    style={{ width: `${Math.round(f.confidence * 100)}%` }}
                  />
                </div>
                <span className="finding-pct">{Math.round(f.confidence * 100)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {diagnosis.meets_threshold === false && (
        <p className="alert alert-warn">Low confidence — try a clearer, well-lit teeth photo.</p>
      )}
      {analysis.model_id === "stub-fallback" && (
        <p className="alert alert-warn">
          Gemini unavailable — showing placeholder data. Check API key and restart backend.
        </p>
      )}

      <p className="disclaimer">{diagnosis.disclaimer}</p>
    </aside>
  );
}
