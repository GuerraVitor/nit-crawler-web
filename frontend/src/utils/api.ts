import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api"; // URL do backend

export const fetchArticles = async () => {
  const response = await axios.get(`${BASE_URL}/articles/`);
  return response.data;
};

export const fetchProjects = async () => {
  const response = await axios.get(`${BASE_URL}/projects/`);
  return response.data;
};

export const fetchProjectById = async (id: string) => {
  const response = await axios.get(`${BASE_URL}/projects/${id}/`);
  return response.data;
};

export const searchResearchers = async (query: string) => {
  const response = await axios.get(`${BASE_URL}/researchers/search/`, {
    params: { q: query },
  });
  return response.data;
};

// URL raiz do backend (sem o sufixo /api), usada para acessar o relatório
// estático do scriptLattes servido em /media/.
const BACKEND_ROOT_URL = BASE_URL.replace(/\/api\/?$/, "");

export const triggerLattesReport = async (extraIds: string[]) => {
  const response = await axios.post(`${BASE_URL}/researchers/lattes-report/`, {
    extra_ids: extraIds,
  });
  return response.data;
};

export const getLattesReportStatus = async () => {
  const response = await axios.get(`${BASE_URL}/researchers/lattes-report/status/`);
  const data = response.data;
  return {
    ...data,
    report_url: data.report_url ? `${BACKEND_ROOT_URL}${data.report_url}` : null,
  };
};
