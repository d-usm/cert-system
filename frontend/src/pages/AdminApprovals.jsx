import { useEffect, useState } from "react";
import api from "../services/api";

export default function AdminApprovals() {
  const [items, setItems] = useState([]);

  const loadPending = async () => {
    try {
      const res = api.get("/admin/pending-exams").then(res => {
        setItems(res.data);
      });
    } catch (err) {
      console.error("Error loading pending exams", err);
    }
  };

  const approve = async (id) => {
    if (!window.confirm("Утвердить результат и выдать сертификат?")) return;

    try {
      const res = await api.post(`/admin/approve/${id}`);
      alert("Сертификат создан!");
      loadPending();
    } catch (err) {
      console.error("Approve error", err);
      alert("Ошибка при утверждении");
    }
  };

  useEffect(() => {
    loadPending();
  }, []);

  return (
    <div className="container mt-4">
      <h3 className="mb-3">Заявки на утверждение</h3>

      <table className="table table-bordered table-sm">
        <thead>
          <tr>
            <th>ID</th>
            <th>Студент</th>
            <th>Курс</th>
            <th>Сдан</th>
            <th>Дата</th>
            <th>Действия</th>
          </tr>
        </thead>

        <tbody>
          {items.length === 0 && (
            <tr>
              <td colSpan="6" className="text-center">
                Нет заявок
              </td>
            </tr>
          )}

          {items.map((x) => (
            <tr key={x.id}>
              <td>{x.id}</td>
              <td>{x.student_id}</td>
              <td>{x.course_id}</td>
              <td>{x.is_passed ? "Да" : "Нет"}</td>
              <td>{new Date(x.created_at).toLocaleString()}</td>
              <td>
                {x.is_passed ? (
                  <button
                    className="btn btn-success btn-sm"
                    onClick={() => approve(x.id)}
                  >
                    Утвердить
                  </button>
                ) : (
                  <span className="text-muted">Не сдал</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

