import { defineStore } from "pinia";
import { login as apiLogin, refresh as apiRefresh , getProfile } from "@/api/auth";
import type { Role } from "@/types/api";

type AuthState = {
  accessToken: string | null;g
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

    async login(email: string, password: string) {
      const { access, refresh } = await apiLogin(email, password);
      this.accessToken = access;
      this.refreshToken = refresh;
      this.email = email;

     const userData = await getProfile();
      this.email = userData.email;
      this.role = userData.role;

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
