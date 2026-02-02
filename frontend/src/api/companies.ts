import { http } from "./http";
import type { Company, Paginated } from "@/types/api";

function unwrap<T>(data: any): T[] {
  return Array.isArray(data) ? data : (data as Paginated<T>).results;
}

export async function listCompanies(): Promise<Company[]> {
  const res = await http.get("/companies/");
  return unwrap<Company>(res.data);
}

export async function getCompany(id: number): Promise<Company> {
  const res = await http.get(`/companies/${id}/`);
  return res.data;
}

export async function createCompany(payload: { name: string }): Promise<Company> {
  const res = await http.post("/companies/", payload);
  return res.data;
}

export async function updateCompany(id: number, payload: { name: string }): Promise<Company> {
  const res = await http.put(`/companies/${id}/`, payload);
  return res.data;
}

export async function deleteCompany(id: number): Promise<void> {
  await http.delete(`/companies/${id}/`);
}
