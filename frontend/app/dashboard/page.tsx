"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import {
  User,
  Briefcase,
  GraduationCap,
  Wrench,
  FolderGit2,
  Award,
  Languages,
  Plus,
} from "lucide-react";

export default function DashboardPage() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.profile
      .get()
      .then(setProfile)
      .catch(() => setProfile(null))
      .finally(() => setLoading(false));
  }, []);

  const stats = [
    {
      label: "Experiences",
      count: profile?.experiences?.length || 0,
      icon: Briefcase,
      href: "/dashboard/profile#experiences",
      color: "text-blue-600 bg-blue-50",
    },
    {
      label: "Education",
      count: profile?.education_entries?.length || 0,
      icon: GraduationCap,
      href: "/dashboard/profile#education",
      color: "text-green-600 bg-green-50",
    },
    {
      label: "Skills",
      count: profile?.skills?.length || 0,
      icon: Wrench,
      href: "/dashboard/profile#skills",
      color: "text-purple-600 bg-purple-50",
    },
    {
      label: "Projects",
      count: profile?.projects?.length || 0,
      icon: FolderGit2,
      href: "/dashboard/profile#projects",
      color: "text-orange-600 bg-orange-50",
    },
    {
      label: "Certifications",
      count: profile?.certifications?.length || 0,
      icon: Award,
      href: "/dashboard/profile#certifications",
      color: "text-yellow-600 bg-yellow-50",
    },
    {
      label: "Languages",
      count: profile?.languages?.length || 0,
      icon: Languages,
      href: "/dashboard/profile#languages",
      color: "text-pink-600 bg-pink-50",
    },
  ];

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  if (!profile) {
    return (
      <div className="text-center py-12">
        <User className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold mb-2">No profile yet</h2>
        <p className="text-gray-600 mb-6">Create your profile to start building ATS-optimized CVs.</p>
        <Link href="/dashboard/profile" className="btn-primary">
          Create Profile
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome, {profile.full_name || "User"}</p>
        </div>
        <Link href="/dashboard/generate" className="btn-primary">
          Generate CV
        </Link>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {stats.map((stat) => (
          <Link
            key={stat.label}
            href={stat.href}
            className="card hover:shadow-md transition-shadow"
          >
            <div className={`w-10 h-10 rounded-lg ${stat.color} flex items-center justify-center mb-3`}>
              <stat.icon className="w-5 h-5" />
            </div>
            <p className="text-2xl font-bold">{stat.count}</p>
            <p className="text-sm text-gray-600">{stat.label}</p>
          </Link>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="font-semibold mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <Link href="/dashboard/profile" className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50">
              <Plus className="w-5 h-5 text-primary-600" />
              <span>Add experience or education</span>
            </Link>
            <Link href="/dashboard/job-offers" className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50">
              <Briefcase className="w-5 h-5 text-primary-600" />
              <span>Paste a job offer to analyze</span>
            </Link>
            <Link href="/dashboard/generate" className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50">
              <FolderGit2 className="w-5 h-5 text-primary-600" />
              <span>Generate optimized CV</span>
            </Link>
          </div>
        </div>

        <div className="card">
          <h3 className="font-semibold mb-4">Profile Status</h3>
          <div className="space-y-3">
            {profile.full_name ? (
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500" />
                <span className="text-sm">Name: {profile.full_name}</span>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-yellow-500" />
                <span className="text-sm">Add your name</span>
              </div>
            )}
            {profile.professional_summary ? (
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500" />
                <span className="text-sm">Professional summary set</span>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-yellow-500" />
                <span className="text-sm">Add professional summary</span>
              </div>
            )}
            {(profile.experiences?.length || 0) > 0 ? (
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500" />
                <span className="text-sm">{profile.experiences.length} experience(s)</span>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-red-500" />
                <span className="text-sm">No experiences added</span>
              </div>
            )}
            {(profile.skills?.length || 0) > 0 ? (
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500" />
                <span className="text-sm">{profile.skills.length} skill(s)</span>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-red-500" />
                <span className="text-sm">No skills added</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
