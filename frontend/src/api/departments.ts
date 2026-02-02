import { http } from "./http";
import type { Department, Paginated } from "@/types/api";

function unwrap<T>(data: any): T[] {
  return Array.isArray(data) ? data : (data as Paginated<T>).results;
}

export async function listDepartments(companyId?: number): Promise<Department[]> {
  const res = await http.get("/departments/", {
    params: companyId ? { company: companyId } : undefined,
  });
  return unwrap<Department>(res.data);

}

export async function getDepartment(id: number): Promise<Department> {
  const res = await http.get(`/departments/${id}/`);
  return res.data;
}

export async function createDepartment(payload: { name: string }): Promise<Department> {
  const res = await http.post("/departments/", payload);
  return res.data;
}

export async function updateDepartment(id: number, payload: { name: string }): Promise<Department> {
  const res = await http.put(`/departments/${id}/`, payload);
  return res.data;
}

export async function deleteDepartment(id: number): Promise<void> {
  await http.delete(`/departments/${id}/`);
}

