const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function getHeaders(): HeadersInit {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }
  return headers;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...getHeaders(),
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  if (response.status === 204) return undefined as T;

  return response.json();
}

export const api = {
  auth: {
    register: (email: string, password: string) =>
      request<{ access_token: string }>("/api/v1/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      }),
    login: (email: string, password: string) =>
      request<{ access_token: string }>("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      }),
    getMe: () => request<import("@/types").User>("/api/v1/auth/me"),
  },

  profile: {
    create: (data: Partial<import("@/types").Profile>) =>
      request<import("@/types").Profile>("/api/v1/profiles", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    get: () => request<import("@/types").Profile & { experiences: import("@/types").Experience[]; education_entries: import("@/types").Education[]; skills: import("@/types").Skill[]; certifications: import("@/types").Certification[]; projects: import("@/types").Project[]; languages: import("@/types").Language[] }>("/api/v1/profiles/me"),
    update: (data: Partial<import("@/types").Profile>) =>
      request<import("@/types").Profile>("/api/v1/profiles/me", {
        method: "PUT",
        body: JSON.stringify(data),
      }),
  },

  experiences: {
    list: () => request<import("@/types").Experience[]>("/api/v1/profiles/me/experiences"),
    create: (data: Omit<import("@/types").Experience, "id" | "profile_id">) =>
      request<import("@/types").Experience>("/api/v1/profiles/me/experiences", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    update: (id: string, data: Partial<import("@/types").Experience>) =>
      request<import("@/types").Experience>(`/api/v1/profiles/me/experiences/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<void>(`/api/v1/profiles/me/experiences/${id}`, {
        method: "DELETE",
      }),
  },

  education: {
    list: () => request<import("@/types").Education[]>("/api/v1/profiles/me/education"),
    create: (data: Omit<import("@/types").Education, "id" | "profile_id">) =>
      request<import("@/types").Education>("/api/v1/profiles/me/education", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    update: (id: string, data: Partial<import("@/types").Education>) =>
      request<import("@/types").Education>(`/api/v1/profiles/me/education/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<void>(`/api/v1/profiles/me/education/${id}`, {
        method: "DELETE",
      }),
  },

  skills: {
    list: () => request<import("@/types").Skill[]>("/api/v1/profiles/me/skills"),
    create: (data: Omit<import("@/types").Skill, "id" | "profile_id">) =>
      request<import("@/types").Skill>("/api/v1/profiles/me/skills", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    update: (id: string, data: Partial<import("@/types").Skill>) =>
      request<import("@/types").Skill>(`/api/v1/profiles/me/skills/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<void>(`/api/v1/profiles/me/skills/${id}`, {
        method: "DELETE",
      }),
  },

  projects: {
    list: () => request<import("@/types").Project[]>("/api/v1/profiles/me/projects"),
    create: (data: Omit<import("@/types").Project, "id" | "profile_id">) =>
      request<import("@/types").Project>("/api/v1/profiles/me/projects", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    update: (id: string, data: Partial<import("@/types").Project>) =>
      request<import("@/types").Project>(`/api/v1/profiles/me/projects/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<void>(`/api/v1/profiles/me/projects/${id}`, {
        method: "DELETE",
      }),
  },

  certifications: {
    list: () => request<import("@/types").Certification[]>("/api/v1/profiles/me/certifications"),
    create: (data: Omit<import("@/types").Certification, "id" | "profile_id">) =>
      request<import("@/types").Certification>("/api/v1/profiles/me/certifications", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    update: (id: string, data: Partial<import("@/types").Certification>) =>
      request<import("@/types").Certification>(`/api/v1/profiles/me/certifications/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<void>(`/api/v1/profiles/me/certifications/${id}`, {
        method: "DELETE",
      }),
  },

  languages: {
    list: () => request<import("@/types").Language[]>("/api/v1/profiles/me/languages"),
    create: (data: Omit<import("@/types").Language, "id" | "profile_id">) =>
      request<import("@/types").Language>("/api/v1/profiles/me/languages", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    update: (id: string, data: Partial<import("@/types").Language>) =>
      request<import("@/types").Language>(`/api/v1/profiles/me/languages/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<void>(`/api/v1/profiles/me/languages/${id}`, {
        method: "DELETE",
      }),
  },

  jobOffers: {
    parse: (rawText: string) =>
      request<import("@/types").JobOffer>("/api/v1/job-offers/parse", {
        method: "POST",
        body: JSON.stringify({ raw_text: rawText }),
      }),
    list: () => request<import("@/types").JobOffer[]>("/api/v1/job-offers"),
    get: (id: string) => request<import("@/types").JobOffer>(`/api/v1/job-offers/${id}`),
    delete: (id: string) =>
      request<void>(`/api/v1/job-offers/${id}`, {
        method: "DELETE",
      }),
  },

  matching: {
    analyze: (jobOfferId: string) =>
      request<import("@/types").MatchResult>("/api/v1/matching/analyze", {
        method: "POST",
        body: JSON.stringify({ job_offer_id: jobOfferId }),
      }),
  },

  generate: {
    generate: (jobOfferId?: string) =>
      request<{ cv_id: string; file_path: string; matching_score: number | null; message: string }>(
        "/api/v1/generate",
        {
          method: "POST",
          body: JSON.stringify({ job_offer_id: jobOfferId }),
        }
      ),
    download: async (cvId: string) => {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${base}/api/v1/generate/${cvId}/download`, {
        headers: getHeaders(),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Download failed" }));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      window.open(url, "_blank");
      setTimeout(() => URL.revokeObjectURL(url), 10000);
    },
    history: () => request<{ id: string; matching_score: number | null; created_at: string; file_path: string }[]>("/api/v1/generate/history"),
  },
};
