export type VisualFinding = {
  label: string;
  confidence: number;
  region?: string | null;
};

export type AnalysisResult = {
  analysis_id: string;
  user_id: string;
  findings: VisualFinding[];
  overall_quality_score: number;
  model_id: string;
  inference_ms: number;
  analyzed_at: string;
};

export type DiagnosisResult = {
  diagnosis_id: string;
  user_id: string;
  analysis_id: string;
  condition_label: string;
  severity: string;
  confidence: number;
  confidence_threshold: number;
  meets_threshold: boolean;
  action_trigger: string;
  disclaimer: string;
  diagnosed_at: string;
};

export type PipelineResult = {
  analysis: AnalysisResult;
  diagnosis: DiagnosisResult;
};
