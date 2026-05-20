"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import { FileText, Zap, Target, Shield } from "lucide-react";

export default function HomePage() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      api.auth.getMe()
        .then(() => setIsLoggedIn(true))
        .catch(() => setIsLoggedIn(false));
    }
  }, []);

  return (
    <div className="min-h-screen">
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <FileText className="w-8 h-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">CV Generator</span>
            </div>
            <div className="flex items-center gap-4">
              {isLoggedIn ? (
                <button onClick={() => router.push("/dashboard")} className="btn-primary">
                  Dashboard
                </button>
              ) : (
                <>
                  <Link href="/login" className="btn-secondary">
                    Login
                  </Link>
                  <Link href="/register" className="btn-primary">
                    Get Started
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <main>
        <section className="py-20 bg-gradient-to-br from-primary-600 to-primary-800 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              ATS-Optimized CVs Powered by AI
            </h1>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Create professional resumes that pass Applicant Tracking Systems.
              AI-powered matching, keyword optimization, and Word template export.
            </p>
            <Link href={isLoggedIn ? "/dashboard" : "/register"} className="btn-primary bg-white text-primary-700 hover:bg-gray-100 text-lg px-8 py-3">
              {isLoggedIn ? "Go to Dashboard" : "Start Free"}
            </Link>
          </div>
        </section>

        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center p-6">
                <Target className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">ATS Optimization</h3>
                <p className="text-gray-600">
                  AI analyzes job offers and optimizes your CV with the right keywords and skills.
                </p>
              </div>
              <div className="text-center p-6">
                <Zap className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Smart Matching</h3>
                <p className="text-gray-600">
                  Semantic matching between your profile and job requirements with scoring.
                </p>
              </div>
              <div className="text-center p-6">
                <Shield className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Professional Templates</h3>
                <p className="text-gray-600">
                  Export to clean Word documents based on proven Harvard-style templates.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
