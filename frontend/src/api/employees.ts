import { http } from "./http";
import type { Employee, Paginated } from "@/types/api";

function unwrap<T>(data: any): T[] {
  return Array.isArray(data) ? data : (data as Paginated<T>).results;
}

export async function listEmployees(params?: {
  company?: number;
  department?: number;
  status?: string;
  search?: string;
}): Promise<Employee[]> {
  // If you implement django-filter / search backend, these will work.
  const res = await http.get("/employees/", { params });
  return unwrap<Employee>(res.data);
}

export async function getEmployee(id: number): Promise<Employee> {
  const res = await http.get(`/employees/${id}/`);
  return res.data;
}
// frontend/src/api/employees.ts
export async function getHiredReport(): Promise<Employee[]> {
  const res = await http.get("/employees/hired_report/");
  return res.data; 
}

export async function createEmployee(payload: Partial<Employee>): Promise<Employee> {
  const res = await http.post("/employees/", payload);
  return res.data;
}

export async function updateEmployee(id: number, payload: Partial<Employee>): Promise<Employee> {
  const res = await http.put(`/employees/${id}/`, payload);
  return res.data;
}

export async function deleteEmployee(id: number): Promise<void> {
  await http.delete(`/employees/${id}/`);
}

export async function transitionEmployee(
  id: number,
  payload: { action: "schedule_interview" | "reject" | "hire"; hired_on?: string }
): Promise<Employee> {
  const res = await http.post(`/employees/${id}/onboard/`, payload);
  return res.data;
}
