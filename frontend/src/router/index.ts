import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
  { path: "/login", name: "login", component: () => import("@/views/LoginView.vue") },

  { path: "/", redirect: "/companies" },

  { path: "/companies", name: "companies", component: () => import("@/views/CompanyListView.vue"), meta: { auth: true } },
  { path: "/companies/:id", name: "company-detail", component: () => import("@/views/CompanyDetailView.vue"), meta: { auth: true } },

  { path: "/departments", name: "departments", component: () => import("@/views/DepartmentListView.vue"), meta: { auth: true } },

  { path: "/employees", name: "employees", component: () => import("@/views/EmployeeListView.vue"), meta: { auth: true } },
  { path: "/employees/new", name: "employee-create", component: () => import("@/views/EmployeeCreateView.vue"), meta: { auth: true, write: true } },
  { path: "/employees/:id", name: "employee-detail", component: () => import("@/views/EmployeeDetailView.vue"), meta: { auth: true } },
  { path: "/employees/:id/edit", name: "employee-edit", component: () => import("@/views/EmployeeEditView.vue"), meta: { auth: true, write: true } },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();

  if (to.meta.auth && !auth.isAuthed) return { name: "login" };
  if (to.meta.write && !auth.canWrite) return { name: "employees" };

  return true;
});
