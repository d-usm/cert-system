import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function AddStudent() {
  const navigate = useNavigate();
  const [fullname, setFullname] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  const createStudent = async () => {
    try {
      await api.post("/operator/create-student", {
        fullname,
        email,
        phone,
      });
      alert("Студент успешно создан");
      navigate("/operator/students");
    } catch (err) {
      console.error(err);
      const msg =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Ошибка при создании студента";
      alert(msg);
    }
  };

  return (
    <div className="container mt-4" style={{ maxWidth: 500 }}>
      <h3 className="mb-3">Добавить студента</h3>

      <div className="mb-3">
        <label className="form-label">ФИО</label>
        <input
          className="form-control"
          value={fullname}
          onChange={(e) => setFullname(e.target.value)}
        />
      </div>

      <div className="mb-3">
        <label className="form-label">Email</label>
        <input
          className="form-control"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div className="mb-3">
        <label className="form-label">Телефон</label>
        <input
          className="form-control"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
        />
      </div>

      <button className="btn btn-success" onClick={createStudent}>
        Создать
      </button>
    </div>
  );
}

