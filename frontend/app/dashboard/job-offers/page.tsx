"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Briefcase, Trash2, Eye, Loader2, AlertCircle } from "lucide-react";

export default function JobOffersPage() {
  const [jobOffers, setJobOffers] = useState<any[]>([]);
  const [rawText, setRawText] = useState("");
  const [loading, setLoading] = useState(false);
  const [parsing, setParsing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadJobOffers();
  }, []);

  const loadJobOffers = async () => {
    try {
      const offers = await api.jobOffers.list();
      setJobOffers(offers);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load job offers");
    }
  };

  const handleParse = async () => {
    if (!rawText.trim()) return;
    setParsing(true);
    setError("");
    try {
      await api.jobOffers.parse(rawText);
      setRawText("");
      loadJobOffers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to parse job offer");
    } finally {
      setParsing(false);
    }
  };

  const handleDelete = async (id: string) => {
    await api.jobOffers.delete(id);
    loadJobOffers();
  };

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-gray-900">Job Offers</h1>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          {error}
        </div>
      )}

      <div className="card">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Briefcase className="w-5 h-5" /> Paste Job Description
        </h2>
        <textarea
          className="input-field"
          rows={8}
          placeholder="Paste the full job description here..."
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
        />
        <button
          onClick={handleParse}
          className="btn-primary mt-3 flex items-center gap-2"
          disabled={parsing || !rawText.trim()}
        >
          {parsing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Eye className="w-4 h-4" />}
          {parsing ? "Analyzing..." : "Analyze Job Offer"}
        </button>
      </div>

      <div className="space-y-4">
        <h2 className="text-lg font-semibold">Parsed Job Offers</h2>
        {jobOffers.map((offer) => (
          <div key={offer.id} className="card">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-semibold text-lg">
                  {offer.title || "Untitled Position"}
                </h3>
                {offer.company && <p className="text-gray-600">{offer.company}</p>}
                {offer.seniority && (
                  <span className="badge badge-info mt-1">{offer.seniority}</span>
                )}
                {offer.parsed_json && (
                  <div className="mt-3 space-y-2">
                    {offer.parsed_json.required_skills && (
                      <div>
                        <span className="text-sm font-medium">Required Skills:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {(offer.parsed_json.required_skills as string[]).map((s, i) => (
                            <span key={i} className="badge badge-success">{s}</span>
                          ))}
                        </div>
                      </div>
                    )}
                    {offer.parsed_json.soft_skills && (
                      <div>
                        <span className="text-sm font-medium">Soft Skills:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {(offer.parsed_json.soft_skills as string[]).map((s, i) => (
                            <span key={i} className="badge badge-warning">{s}</span>
                          ))}
                        </div>
                      </div>
                    )}
                    {offer.parsed_json.keywords && (
                      <div>
                        <span className="text-sm font-medium">Keywords:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {(offer.parsed_json.keywords as string[]).map((s, i) => (
                            <span key={i} className="badge badge-info">{s}</span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
              <button onClick={() => handleDelete(offer.id)} className="text-red-500 hover:text-red-700">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
        {jobOffers.length === 0 && (
          <p className="text-gray-500 text-center py-8">No job offers analyzed yet.</p>
        )}
      </div>
    </div>
  );
}
