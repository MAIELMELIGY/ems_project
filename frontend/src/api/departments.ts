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
