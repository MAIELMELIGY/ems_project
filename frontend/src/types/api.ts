export type Role = "admin" | "manager" | "employee";

export type UserMe = {
  id: number;
  email: string;
  username: string;
  role: Role;
};

export type Company = {
  id: number;
  name: string;
  department_count: number;
  employee_count: number;
  created_at: string;
};

export type Department = {
  id: number;
  company: number;
  name: string;
  employee_count: number;
};

export type EmployeeStatus =
  | "application_received"
  | "interview_scheduled"
  | "hired"
  | "not_accepted";

export type Employee = {
  id: number;
  company: number;
  department: number;
  status: EmployeeStatus;
  name: string;
  email: string;
  mobile: string;
  address: string;
  designation: string;
  hired_on: string | null;
  days_employed: number | null;
  created_at: string;
};

export type Paginated<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};
