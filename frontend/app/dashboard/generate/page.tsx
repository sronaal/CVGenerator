"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Download, Loader2, FileText, BarChart3, AlertCircle } from "lucide-react";

export default function GeneratePage() {
  const [jobOffers, setJobOffers] = useState<any[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<string>("");
  const [generating, setGenerating] = useState(false);
  const [matchResult, setMatchResult] = useState<any>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [cvHistory, setCvHistory] = useState<any[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    loadJobOffers();
    loadCvHistory();
  }, []);

  const loadJobOffers = async () => {
    try {
      const offers = await api.jobOffers.list();
      setJobOffers(offers);
    } catch (err) {
      console.error(err);
    }
  };

  const loadCvHistory = async () => {
    try {
      const history = await api.generate.history();
      setCvHistory(history);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedJobId) {
      setError("Please select a job offer first");
      return;
    }
    setAnalyzing(true);
    setError("");
    try {
      const result = await api.matching.analyze(selectedJobId);
      setMatchResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setAnalyzing(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    setError("");
    try {
      const result = await api.generate.generate(selectedJobId || undefined);
      setCvHistory((prev) => [
        { id: result.cv_id, matching_score: result.matching_score, created_at: new Date().toISOString() },
        ...prev,
      ]);
      alert("CV generated successfully! You can download it from the history below.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Generation failed");
    } finally {
      setGenerating(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-yellow-600";
    return "text-red-600";
  };

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-gray-900">Generate CV</h1>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <AlertCircle className="w-5 h-5" />
          {error}
        </div>
      )}

      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Select Job Offer (Optional)</h2>
        <p className="text-sm text-gray-600 mb-4">
          Select a parsed job offer to generate an ATS-optimized CV. Leave empty for a general CV.
        </p>
        <select
          className="input-field"
          value={selectedJobId}
          onChange={(e) => setSelectedJobId(e.target.value)}
        >
          <option value="">General CV (no job targeting)</option>
          {jobOffers.map((offer) => (
            <option key={offer.id} value={offer.id}>
              {offer.title || "Untitled"} {offer.company ? `at ${offer.company}` : ""}
            </option>
          ))}
        </select>

        <div className="flex gap-3 mt-4">
          <button
            onClick={handleAnalyze}
            className="btn-secondary flex items-center gap-2"
            disabled={analyzing || !selectedJobId}
          >
            {analyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : <BarChart3 className="w-4 h-4" />}
            {analyzing ? "Analyzing..." : "Analyze Match"}
          </button>
          <button
            onClick={handleGenerate}
            className="btn-primary flex items-center gap-2"
            disabled={generating}
          >
            {generating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
            {generating ? "Generating..." : "Generate CV"}
          </button>
        </div>
      </div>

      {matchResult && (
        <div className="card">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <BarChart3 className="w-5 h-5" /> Match Analysis
          </h2>
          <div className="text-center mb-6">
            <div className={`text-5xl font-bold ${getScoreColor(matchResult.overall_score)}`}>
              {matchResult.overall_score}%
            </div>
            <p className="text-gray-600">Overall Match Score</p>
          </div>

          <div className="grid md:grid-cols-4 gap-4 mb-6">
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <p className={`text-2xl font-bold ${getScoreColor(matchResult.hard_skills_score)}`}>
                {matchResult.hard_skills_score}%
              </p>
              <p className="text-sm text-gray-600">Hard Skills</p>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <p className={`text-2xl font-bold ${getScoreColor(matchResult.soft_skills_score)}`}>
                {matchResult.soft_skills_score}%
              </p>
              <p className="text-sm text-gray-600">Soft Skills</p>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <p className={`text-2xl font-bold ${getScoreColor(matchResult.keywords_score)}`}>
                {matchResult.keywords_score}%
              </p>
              <p className="text-sm text-gray-600">Keywords</p>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <p className={`text-2xl font-bold ${getScoreColor(matchResult.seniority_alignment)}`}>
                {matchResult.seniority_alignment}%
              </p>
              <p className="text-sm text-gray-600">Seniority</p>
            </div>
          </div>

          {matchResult.missing_skills.length > 0 && (
            <div className="mb-4">
              <h3 className="font-medium mb-2">Missing Skills</h3>
              <div className="flex flex-wrap gap-2">
                {matchResult.missing_skills.map((skill: string, i: number) => (
                  <span key={i} className="badge badge-danger">{skill}</span>
                ))}
              </div>
            </div>
          )}

          {matchResult.optimization_suggestions.length > 0 && (
            <div>
              <h3 className="font-medium mb-2">Suggestions</h3>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                {matchResult.optimization_suggestions.map((s: string, i: number) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="card">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <FileText className="w-5 h-5" /> CV History
        </h2>
        {cvHistory.length > 0 ? (
          <div className="space-y-3">
            {cvHistory.map((cv) => (
              <div key={cv.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">CV Generated</p>
                  <p className="text-sm text-gray-500">
                    {new Date(cv.created_at).toLocaleDateString()}
                    {cv.matching_score !== null && ` • Match: ${cv.matching_score}%`}
                  </p>
                </div>
                <a
                  href={api.generate.download(cv.id)}
                  className="btn-primary text-sm flex items-center gap-1"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Download className="w-4 h-4" /> Download
                </a>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-4">No CVs generated yet.</p>
        )}
      </div>
    </div>
  );
}
