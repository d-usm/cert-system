import { createContext, useState, useEffect } from "react";
import api from "../services/api";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState({
    token: localStorage.getItem("token") || null,
    role: localStorage.getItem("role") || null,
    fullname: localStorage.getItem("fullname") || null,
    id: localStorage.getItem("id") || null,
  });

  useEffect(() => {
    // можно потом добавить авто-проверку /auth/me при загрузке
  }, []);

  const login = async (email, password) => {
    const params = new URLSearchParams();
    params.append("username", email.trim());
    params.append("password", password.trim());

    // логин
    const res = await api.post("/auth/login", params, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    const token = res.data.access_token;
    localStorage.setItem("token", token);

    // профиль
    const me = await api.get("/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    });

    localStorage.setItem("role", me.data.role);
    localStorage.setItem("fullname", me.data.fullname);
    localStorage.setItem("id", me.data.id);

    setUser({
      token,
      role: me.data.role,
      fullname: me.data.fullname,
      id: me.data.id,
    });
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("fullname");
    localStorage.removeItem("id");
    setUser({ token: null, role: null, fullname: null, id: null });
    window.location.href = "/login";
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

