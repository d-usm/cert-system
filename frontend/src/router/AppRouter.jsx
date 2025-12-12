import { Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../auth/AuthContext";

import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import OperatorStudents from "../pages/OperatorStudents";
import AddStudent from "../pages/AddStudent";
import OperatorExamRecord from "../pages/OperatorExamRecord";
// заглушки для админа — создадим ниже
import AdminApprovals from "../pages/AdminApprovals";
import AdminCertificates from "../pages/AdminCertificates";
import VerifyCertificate from "../pages/VerifyCertificate";
function RequireAuth({ children, roles }) {
  const { user } = useContext(AuthContext);

  if (!user?.token) {
    return <Navigate to="/login" replace />;
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route
        path="/dashboard"
        element={
          <RequireAuth>
            <Dashboard />
          </RequireAuth>
        }
      />

      {/* ОПЕРАТОР */}
      <Route
        path="/operator/students"
        element={
          <RequireAuth roles={["operator", "admin"]}>
            <OperatorStudents />
          </RequireAuth>
        }
      />
      <Route
        path="/operator/add-student"
        element={
          <RequireAuth roles={["operator", "admin"]}>
            <AddStudent />
          </RequireAuth>
        }
      />
      <Route
        path="/operator/exam-record"
        element={
          <RequireAuth roles={["operator", "admin"]}>
            <OperatorExamRecord />
          </RequireAuth>
        }
      />

      {/* АДМИН */}
      <Route
        path="/admin/approvals"
        element={
          <RequireAuth roles={["admin"]}>
            <AdminApprovals />
          </RequireAuth>
        }
      />
      <Route
        path="/admin/certificates"
        element={
          <RequireAuth roles={["admin"]}>
            <AdminCertificates />
          </RequireAuth>
        }
      />
      <Route path="/verify/:token" element={<VerifyCertificate />} />

      {/* дефолт */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

