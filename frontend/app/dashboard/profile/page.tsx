"use client";

import { useEffect, useState } from "react";
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
  Edit2,
  Trash2,
  Save,
  X,
} from "lucide-react";

type ProfileData = {
  id: string;
  full_name: string | null;
  email: string | null;
  phone: string | null;
  location: string | null;
  linkedin_url: string | null;
  portfolio_url: string | null;
  professional_summary: string | null;
};

export default function ProfilePage() {
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [experiences, setExperiences] = useState<any[]>([]);
  const [education, setEducation] = useState<any[]>([]);
  const [skills, setSkills] = useState<any[]>([]);
  const [projects, setProjects] = useState<any[]>([]);
  const [certifications, setCertifications] = useState<any[]>([]);
  const [languages, setLanguages] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingProfile, setEditingProfile] = useState(false);
  const [profileForm, setProfileForm] = useState<Partial<ProfileData>>({});

  const [showExperienceForm, setShowExperienceForm] = useState(false);
  const [showEducationForm, setShowEducationForm] = useState(false);
  const [showSkillForm, setShowSkillForm] = useState(false);
  const [showProjectForm, setShowProjectForm] = useState(false);
  const [showCertificationForm, setShowCertificationForm] = useState(false);
  const [showLanguageForm, setShowLanguageForm] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const p = await api.profile.get();
      setProfile(p);
      setProfileForm({
        full_name: p.full_name,
        email: p.email,
        phone: p.phone,
        location: p.location,
        linkedin_url: p.linkedin_url,
        portfolio_url: p.portfolio_url,
        professional_summary: p.professional_summary,
      });
      setExperiences(p.experiences || []);
      setEducation(p.education_entries || []);
      setSkills(p.skills || []);
      setProjects(p.projects || []);
      setCertifications(p.certifications || []);
      setLanguages(p.languages || []);
    } catch {
      try {
        await api.profile.create({});
        loadData();
      } catch {
        setLoading(false);
      }
    } finally {
      setLoading(false);
    }
  };

  const saveProfile = async () => {
    await api.profile.update(profileForm);
    setEditingProfile(false);
    loadData();
  };

  const deleteExperience = async (id: string) => {
    await api.experiences.delete(id);
    setExperiences((prev) => prev.filter((e) => e.id !== id));
  };

  const deleteEducation = async (id: string) => {
    await api.education.delete(id);
    setEducation((prev) => prev.filter((e) => e.id !== id));
  };

  const deleteSkill = async (id: string) => {
    await api.skills.delete(id);
    setSkills((prev) => prev.filter((s) => s.id !== id));
  };

  const deleteProject = async (id: string) => {
    await api.projects.delete(id);
    setProjects((prev) => prev.filter((p) => p.id !== id));
  };

  const deleteCertification = async (id: string) => {
    await api.certifications.delete(id);
    setCertifications((prev) => prev.filter((c) => c.id !== id));
  };

  const deleteLanguage = async (id: string) => {
    await api.languages.delete(id);
    setLanguages((prev) => prev.filter((l) => l.id !== id));
  };

  if (loading) return <div className="text-center py-12">Loading...</div>;

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-gray-900">Profile Management</h1>

      {/* Profile Info */}
      <section id="profile" className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <User className="w-5 h-5" /> Personal Information
          </h2>
          <button
            onClick={() => setEditingProfile(!editingProfile)}
            className="btn-secondary text-sm"
          >
            {editingProfile ? <X className="w-4 h-4" /> : <Edit2 className="w-4 h-4" />}
          </button>
        </div>

        {editingProfile ? (
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="label">Full Name</label>
              <input
                className="input-field"
                value={profileForm.full_name || ""}
                onChange={(e) => setProfileForm({ ...profileForm, full_name: e.target.value })}
              />
            </div>
            <div>
              <label className="label">Email</label>
              <input
                className="input-field"
                type="email"
                value={profileForm.email || ""}
                onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })}
              />
            </div>
            <div>
              <label className="label">Phone</label>
              <input
                className="input-field"
                value={profileForm.phone || ""}
                onChange={(e) => setProfileForm({ ...profileForm, phone: e.target.value })}
              />
            </div>
            <div>
              <label className="label">Location</label>
              <input
                className="input-field"
                value={profileForm.location || ""}
                onChange={(e) => setProfileForm({ ...profileForm, location: e.target.value })}
              />
            </div>
            <div>
              <label className="label">LinkedIn URL</label>
              <input
                className="input-field"
                value={profileForm.linkedin_url || ""}
                onChange={(e) => setProfileForm({ ...profileForm, linkedin_url: e.target.value })}
              />
            </div>
            <div>
              <label className="label">Portfolio URL</label>
              <input
                className="input-field"
                value={profileForm.portfolio_url || ""}
                onChange={(e) => setProfileForm({ ...profileForm, portfolio_url: e.target.value })}
              />
            </div>
            <div className="md:col-span-2">
              <label className="label">Professional Summary</label>
              <textarea
                className="input-field"
                rows={3}
                value={profileForm.professional_summary || ""}
                onChange={(e) => setProfileForm({ ...profileForm, professional_summary: e.target.value })}
              />
            </div>
            <div className="md:col-span-2 flex gap-2">
              <button onClick={saveProfile} className="btn-primary flex items-center gap-1">
                <Save className="w-4 h-4" /> Save
              </button>
              <button onClick={() => setEditingProfile(false)} className="btn-secondary">
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div><span className="font-medium">Name:</span> {profile?.full_name || "—"}</div>
            <div><span className="font-medium">Email:</span> {profile?.email || "—"}</div>
            <div><span className="font-medium">Phone:</span> {profile?.phone || "—"}</div>
            <div><span className="font-medium">Location:</span> {profile?.location || "—"}</div>
            <div><span className="font-medium">LinkedIn:</span> {profile?.linkedin_url || "—"}</div>
            <div><span className="font-medium">Portfolio:</span> {profile?.portfolio_url || "—"}</div>
            <div className="md:col-span-2">
              <span className="font-medium">Summary:</span>
              <p className="mt-1 text-gray-600">{profile?.professional_summary || "—"}</p>
            </div>
          </div>
        )}
      </section>

      {/* Experiences */}
      <section id="experiences" className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Briefcase className="w-5 h-5" /> Experience
          </h2>
          <button onClick={() => setShowExperienceForm(!showExperienceForm)} className="btn-primary text-sm flex items-center gap-1">
            <Plus className="w-4 h-4" /> Add
          </button>
        </div>

        {showExperienceForm && <ExperienceForm onSuccess={() => { setShowExperienceForm(false); loadData(); }} />}

        <div className="space-y-4">
          {experiences.map((exp) => (
            <div key={exp.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex justify-between">
                <div>
                  <h3 className="font-semibold">{exp.title}</h3>
                  <p className="text-sm text-gray-600">{exp.company} • {exp.location}</p>
                  <p className="text-xs text-gray-500">
                    {exp.start_date} → {exp.is_current ? "Present" : exp.end_date || "Present"}
                  </p>
                </div>
                <button onClick={() => deleteExperience(exp.id)} className="text-red-500 hover:text-red-700">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
              {exp.bullets?.length > 0 && (
                <ul className="mt-2 list-disc list-inside text-sm text-gray-600">
                  {exp.bullets.map((b: string, i: number) => (
                    <li key={i}>{b}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
          {experiences.length === 0 && <p className="text-gray-500 text-sm">No experiences added yet.</p>}
        </div>
      </section>

      {/* Education */}
      <section id="education" className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <GraduationCap className="w-5 h-5" /> Education
          </h2>
          <button onClick={() => setShowEducationForm(!showEducationForm)} className="btn-primary text-sm flex items-center gap-1">
            <Plus className="w-4 h-4" /> Add
          </button>
        </div>

        {showEducationForm && <EducationForm onSuccess={() => { setShowEducationForm(false); loadData(); }} />}

        <div className="space-y-4">
          {education.map((edu) => (
            <div key={edu.id} className="border border-gray-200 rounded-lg p-4 flex justify-between">
              <div>
                <h3 className="font-semibold">{edu.institution}</h3>
                <p className="text-sm text-gray-600">
                  {edu.degree} {edu.field_of_study ? `in ${edu.field_of_study}` : ""}
                </p>
                {edu.gpa && <p className="text-xs text-gray-500">GPA: {edu.gpa}</p>}
              </div>
              <button onClick={() => deleteEducation(edu.id)} className="text-red-500 hover:text-red-700">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
          {education.length === 0 && <p className="text-gray-500 text-sm">No education entries added yet.</p>}
        </div>
      </section>

      {/* Skills */}
      <section id="skills" className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Wrench className="w-5 h-5" /> Skills
          </h2>
          <button onClick={() => setShowSkillForm(!showSkillForm)} className="btn-primary text-sm flex items-center gap-1">
            <Plus className="w-4 h-4" /> Add
          </button>
        </div>

        {showSkillForm && <SkillForm onSuccess={() => { setShowSkillForm(false); loadData(); }} />}

        <div className="flex flex-wrap gap-2">
          {skills.map((skill) => (
            <span
              key={skill.id}
              className="inline-flex items-center gap-1 px-3 py-1 bg-primary-50 text-primary-700 rounded-full text-sm"
            >
              {skill.name}
              <button onClick={() => deleteSkill(skill.id)} className="hover:text-red-600">
                <X className="w-3 h-3" />
              </button>
            </span>
          ))}
          {skills.length === 0 && <p className="text-gray-500 text-sm">No skills added yet.</p>}
        </div>
      </section>

      {/* Projects */}
      <section id="projects" className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <FolderGit2 className="w-5 h-5" /> Projects
          </h2>
          <button onClick={() => setShowProjectForm(!showProjectForm)} className="btn-primary text-sm flex items-center gap-1">
            <Plus className="w-4 h-4" /> Add
          </button>
        </div>

        {showProjectForm && <ProjectForm onSuccess={() => { setShowProjectForm(false); loadData(); }} />}

        <div className="space-y-4">
          {projects.map((project) => (
            <div key={project.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex justify-between">
                <div>
                  <h3 className="font-semibold">{project.name}</h3>
                  {project.description && <p className="text-sm text-gray-600">{project.description}</p>}
                  {project.technologies?.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {project.technologies.map((t: string, i: number) => (
                        <span key={i} className="badge badge-info">{t}</span>
                      ))}
                    </div>
                  )}
                </div>
                <button onClick={() => deleteProject(project.id)} className="text-red-500 hover:text-red-700">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
              {project.bullets?.length > 0 && (
                <ul className="mt-2 list-disc list-inside text-sm text-gray-600">
                  {project.bullets.map((b: string, i: number) => (
                    <li key={i}>{b}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
          {projects.length === 0 && <p className="text-gray-500 text-sm">No projects added yet.</p>}
        </div>
      </section>

      {/* Certifications */}
      <section id="certifications" className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Award className="w-5 h-5" /> Certifications
          </h2>
          <button onClick={() => setShowCertificationForm(!showCertificationForm)} className="btn-primary text-sm flex items-center gap-1">
            <Plus className="w-4 h-4" /> Add
          </button>
        </div>

        {showCertificationForm && <CertificationForm onSuccess={() => { setShowCertificationForm(false); loadData(); }} />}

        <div className="space-y-4">
          {certifications.map((cert) => (
            <div key={cert.id} className="border border-gray-200 rounded-lg p-4 flex justify-between">
              <div>
                <h3 className="font-semibold">{cert.name}</h3>
                <p className="text-sm text-gray-600">{cert.issuing_organization}</p>
              </div>
              <button onClick={() => deleteCertification(cert.id)} className="text-red-500 hover:text-red-700">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
          {certifications.length === 0 && <p className="text-gray-500 text-sm">No certifications added yet.</p>}
        </div>
      </section>

      {/* Languages */}
      <section id="languages" className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Languages className="w-5 h-5" /> Languages
          </h2>
          <button onClick={() => setShowLanguageForm(!showLanguageForm)} className="btn-primary text-sm flex items-center gap-1">
            <Plus className="w-4 h-4" /> Add
          </button>
        </div>

        {showLanguageForm && <LanguageForm onSuccess={() => { setShowLanguageForm(false); loadData(); }} />}

        <div className="flex flex-wrap gap-2">
          {languages.map((lang) => (
            <span
              key={lang.id}
              className="inline-flex items-center gap-1 px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm"
            >
              {lang.language_name} ({lang.proficiency})
              <button onClick={() => deleteLanguage(lang.id)} className="hover:text-red-600">
                <X className="w-3 h-3" />
              </button>
            </span>
          ))}
          {languages.length === 0 && <p className="text-gray-500 text-sm">No languages added yet.</p>}
        </div>
      </section>
    </div>
  );
}

function ExperienceForm({ onSuccess }: { onSuccess: () => void }) {
  const [form, setForm] = useState({
    company: "",
    title: "",
    location: "",
    start_date: "",
    end_date: "",
    is_current: false,
    bullets: [""],
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.experiences.create({
        ...form,
        bullets: form.bullets.filter((b) => b.trim()),
        start_date: form.start_date,
        end_date: form.is_current ? null : form.end_date || null,
      });
      onSuccess();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 rounded-lg p-4 mb-4 space-y-3">
      <div className="grid md:grid-cols-2 gap-3">
        <input className="input-field" placeholder="Company" value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} required />
        <input className="input-field" placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
        <input className="input-field" placeholder="Location" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} />
        <input className="input-field" type="date" placeholder="Start Date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} required />
        {!form.is_current && (
          <input className="input-field" type="date" placeholder="End Date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} />
        )}
        <label className="flex items-center gap-2">
          <input type="checkbox" checked={form.is_current} onChange={(e) => setForm({ ...form, is_current: e.target.checked })} />
          <span className="text-sm">Current position</span>
        </label>
      </div>
      <div>
        <label className="label">Bullets (one per line)</label>
        {form.bullets.map((b, i) => (
          <input
            key={i}
            className="input-field mb-1"
            placeholder={`Bullet ${i + 1}`}
            value={b}
            onChange={(e) => {
              const newBullets = [...form.bullets];
              newBullets[i] = e.target.value;
              setForm({ ...form, bullets: newBullets });
            }}
          />
        ))}
        <button
          type="button"
          className="text-sm text-primary-600"
          onClick={() => setForm({ ...form, bullets: [...form.bullets, ""] })}
        >
          + Add bullet
        </button>
      </div>
      <div className="flex gap-2">
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? "Saving..." : "Save"}
        </button>
      </div>
    </form>
  );
}

function EducationForm({ onSuccess }: { onSuccess: () => void }) {
  const [form, setForm] = useState({
    institution: "",
    degree: "",
    field_of_study: "",
    gpa: "",
    start_date: "",
    end_date: "",
    honors: [""],
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.education.create({
        ...form,
        honors: form.honors.filter((h) => h.trim()),
        start_date: form.start_date || null,
        end_date: form.end_date || null,
      });
      onSuccess();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 rounded-lg p-4 mb-4 space-y-3">
      <div className="grid md:grid-cols-2 gap-3">
        <input className="input-field" placeholder="Institution" value={form.institution} onChange={(e) => setForm({ ...form, institution: e.target.value })} required />
        <input className="input-field" placeholder="Degree" value={form.degree} onChange={(e) => setForm({ ...form, degree: e.target.value })} />
        <input className="input-field" placeholder="Field of Study" value={form.field_of_study} onChange={(e) => setForm({ ...form, field_of_study: e.target.value })} />
        <input className="input-field" placeholder="GPA" value={form.gpa} onChange={(e) => setForm({ ...form, gpa: e.target.value })} />
        <input className="input-field" type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} />
        <input className="input-field" type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} />
      </div>
      <div className="flex gap-2">
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? "Saving..." : "Save"}
        </button>
      </div>
    </form>
  );
}

function SkillForm({ onSuccess }: { onSuccess: () => void }) {
  const [form, setForm] = useState({
    name: "",
    category: "hard",
    proficiency_level: 3,
    years_of_experience: "",
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.skills.create({
        ...form,
        years_of_experience: form.years_of_experience ? parseInt(form.years_of_experience) : null,
      });
      onSuccess();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 rounded-lg p-4 mb-4 space-y-3">
      <div className="grid md:grid-cols-4 gap-3">
        <input className="input-field" placeholder="Skill name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <select className="input-field" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
          <option value="hard">Hard Skill</option>
          <option value="soft">Soft Skill</option>
          <option value="technical">Technical</option>
        </select>
        <input className="input-field" type="number" min="1" max="5" value={form.proficiency_level} onChange={(e) => setForm({ ...form, proficiency_level: parseInt(e.target.value) })} />
        <input className="input-field" type="number" placeholder="Years" value={form.years_of_experience} onChange={(e) => setForm({ ...form, years_of_experience: e.target.value })} />
      </div>
      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? "Saving..." : "Save"}
      </button>
    </form>
  );
}

function ProjectForm({ onSuccess }: { onSuccess: () => void }) {
  const [form, setForm] = useState({
    name: "",
    description: "",
    technologies: "",
    url: "",
    start_date: "",
    end_date: "",
    is_current: false,
    bullets: [""],
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.projects.create({
        name: form.name,
        description: form.description || null,
        technologies: form.technologies.split(",").map((t) => t.trim()).filter(Boolean),
        url: form.url || null,
        start_date: form.start_date || null,
        end_date: form.is_current ? null : form.end_date || null,
        is_current: form.is_current,
        bullets: form.bullets.filter((b) => b.trim()),
      });
      onSuccess();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 rounded-lg p-4 mb-4 space-y-3">
      <div className="grid md:grid-cols-2 gap-3">
        <input className="input-field" placeholder="Project Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <input className="input-field" placeholder="URL" value={form.url} onChange={(e) => setForm({ ...form, url: e.target.value })} />
        <input className="input-field" placeholder="Technologies (comma separated)" value={form.technologies} onChange={(e) => setForm({ ...form, technologies: e.target.value })} />
        <input className="input-field" type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} />
        {!form.is_current && (
          <input className="input-field" type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} />
        )}
        <label className="flex items-center gap-2">
          <input type="checkbox" checked={form.is_current} onChange={(e) => setForm({ ...form, is_current: e.target.checked })} />
          <span className="text-sm">Current project</span>
        </label>
      </div>
      <textarea className="input-field" placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} rows={2} />
      <div>
        <label className="label">Bullets (one per line)</label>
        {form.bullets.map((b, i) => (
          <input
            key={i}
            className="input-field mb-1"
            placeholder={`Bullet ${i + 1}`}
            value={b}
            onChange={(e) => {
              const newBullets = [...form.bullets];
              newBullets[i] = e.target.value;
              setForm({ ...form, bullets: newBullets });
            }}
          />
        ))}
        <button type="button" className="text-sm text-primary-600" onClick={() => setForm({ ...form, bullets: [...form.bullets, ""] })}>
          + Add bullet
        </button>
      </div>
      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? "Saving..." : "Save"}
      </button>
    </form>
  );
}

function CertificationForm({ onSuccess }: { onSuccess: () => void }) {
  const [form, setForm] = useState({
    name: "",
    issuing_organization: "",
    issue_date: "",
    expiry_date: "",
    credential_url: "",
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.certifications.create({
        ...form,
        issue_date: form.issue_date || null,
        expiry_date: form.expiry_date || null,
        credential_url: form.credential_url || null,
      });
      onSuccess();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 rounded-lg p-4 mb-4 space-y-3">
      <div className="grid md:grid-cols-2 gap-3">
        <input className="input-field" placeholder="Certification Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <input className="input-field" placeholder="Issuing Organization" value={form.issuing_organization} onChange={(e) => setForm({ ...form, issuing_organization: e.target.value })} />
        <input className="input-field" type="date" value={form.issue_date} onChange={(e) => setForm({ ...form, issue_date: e.target.value })} />
        <input className="input-field" type="date" value={form.expiry_date} onChange={(e) => setForm({ ...form, expiry_date: e.target.value })} />
        <input className="input-field md:col-span-2" placeholder="Credential URL" value={form.credential_url} onChange={(e) => setForm({ ...form, credential_url: e.target.value })} />
      </div>
      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? "Saving..." : "Save"}
      </button>
    </form>
  );
}

function LanguageForm({ onSuccess }: { onSuccess: () => void }) {
  const [form, setForm] = useState({
    language_name: "",
    proficiency: "intermediate",
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.languages.create(form);
      onSuccess();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 rounded-lg p-4 mb-4 space-y-3">
      <div className="grid md:grid-cols-2 gap-3">
        <input className="input-field" placeholder="Language" value={form.language_name} onChange={(e) => setForm({ ...form, language_name: e.target.value })} required />
        <select className="input-field" value={form.proficiency} onChange={(e) => setForm({ ...form, proficiency: e.target.value })}>
          <option value="native">Native</option>
          <option value="fluent">Fluent</option>
          <option value="intermediate">Intermediate</option>
          <option value="basic">Basic</option>
        </select>
      </div>
      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? "Saving..." : "Save"}
      </button>
    </form>
  );
}
