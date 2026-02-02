import { defineStore } from "pinia";
import { login as apiLogin, refresh as apiRefresh } from "@/api/auth";
import type { Role } from "@/types/api";

type AuthState = {
  accessToken: string | null;
  refreshToken: string | null;
  role: Role | null;
  email: string | null;
};

const LS_KEY = "ems_auth_v1";

function load(): AuthState {
  try {
    return JSON.parse(localStorage.getItem(LS_KEY) || "null") ?? {
      accessToken: null,
      refreshToken: null,
      role: null,
      email: null,
    };
  } catch {
    return { accessToken: null, refreshToken: null, role: null, email: null };
  }
}

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => load(),
  getters: {
    isAuthed: (s) => !!s.accessToken,
    canWrite: (s) => s.role === "admin" || s.role === "manager",
  },
  actions: {
    persist() {
      localStorage.setItem(LS_KEY, JSON.stringify(this.$state));
    },
    clear() {
      this.accessToken = null;
      this.refreshToken = null;
      this.role = null;
      this.email = null;
      this.persist();
    },
    // NOTE: This assumes your backend returns role somehow.
    // Common options:
    // 1) embed role in JWT claims
    // 2) call /me/ after login
    async login(email: string, password: string) {
      const { access, refresh } = await apiLogin(email, password);
      this.accessToken = access;
      this.refreshToken = refresh;
      this.email = email;

      // Minimal placeholder: default role if you don't have /me yet.
      // Replace with real role fetch (recommended).
      // this.role = this.role ?? "employee";

      this.persist();
    },
    async refreshAccessToken() {
      if (!this.refreshToken) throw new Error("Missing refresh token");
      const { access } = await apiRefresh(this.refreshToken);
      this.accessToken = access;
      this.persist();
    },
    setRole(role: Role) {
      this.role = role;
      this.persist();
    },
  },
});
