import { useEffect, useState } from "react";
import api from "../services/api";
import { Link } from "react-router-dom";

export default function OperatorStudents() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    loadStudents();
  }, []);

  const loadStudents = async () => {
    try {
      const res = await api.get("/operator/students");
      setStudents(res.data);
    } catch (e) {
      console.error("Failed to load students", e);
    }
  };

  return (
    <div className="container mt-4">
      <h3 className="mb-3">Студенты</h3>

      <Link to="/operator/add-student" className="btn btn-success mb-3">
        ➕ Добавить студента
      </Link>

      <table className="table table-bordered table-sm">
        <thead>
          <tr>
            <th>ID</th>
            <th>ФИО</th>
            <th>Email</th>
            <th>Телефон</th>
            <th>Дата регистрации</th>
          </tr>
        </thead>
        <tbody>
          {students.map((s) => (
            <tr key={s.id}>
              <td>{s.id}</td>
              <td>{s.fullname}</td>
              <td>{s.email}</td>
              <td>{s.phone}</td>
              <td>
                {s.created_at
                  ? new Date(s.created_at).toLocaleString()
                  : "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

