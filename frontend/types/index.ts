export interface User {
  id: string;
  email: string;
  is_active: string;
}

export interface Profile {
  id: string;
  user_id: string;
  full_name: string | null;
  email: string | null;
  phone: string | null;
  location: string | null;
  linkedin_url: string | null;
  portfolio_url: string | null;
  professional_summary: string | null;
}

export interface Experience {
  id: string;
  profile_id: string;
  company: string;
  title: string;
  location: string | null;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  bullets: string[];
  raw_description: string | null;
}

export interface Education {
  id: string;
  profile_id: string;
  institution: string;
  degree: string | null;
  field_of_study: string | null;
  gpa: string | null;
  start_date: string | null;
  end_date: string | null;
  honors: string[];
}

export interface Skill {
  id: string;
  profile_id: string;
  name: string;
  category: string;
  proficiency_level: number;
  years_of_experience: number | null;
}

export interface Certification {
  id: string;
  profile_id: string;
  name: string;
  issuing_organization: string | null;
  issue_date: string | null;
  expiry_date: string | null;
  credential_url: string | null;
}

export interface Project {
  id: string;
  profile_id: string;
  name: string;
  description: string | null;
  technologies: string[];
  url: string | null;
  start_date: string | null;
  end_date: string | null;
  is_current: boolean;
  bullets: string[];
}

export interface Language {
  id: string;
  profile_id: string;
  language_name: string;
  proficiency: string;
}

export interface JobOffer {
  id: string;
  profile_id: string;
  raw_text: string;
  title: string | null;
  company: string | null;
  seniority: string | null;
  parsed_json: Record<string, unknown> | null;
}

export interface MatchResult {
  overall_score: number;
  hard_skills_score: number;
  soft_skills_score: number;
  keywords_score: number;
  seniority_alignment: number;
  matched_skills: { name: string; matched: boolean; category: string }[];
  missing_skills: string[];
  matched_experiences: string[];
  optimization_suggestions: string[];
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
