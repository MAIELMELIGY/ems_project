import { http } from "./http";

export async function login(email: string, password: string) {
  const res = await http.post("/auth/login/", { email, password });
  return res.data as { access: string; refresh: string };
}

export async function refresh(refreshToken: string) {
  const res = await http.post("/auth/refresh/", { refresh: refreshToken });
  return res.data as { access: string };
}
export async function getProfile() {
  const res = await http.get("/auth/profile/");
  return res.data as { email: string; role: Role };
}
