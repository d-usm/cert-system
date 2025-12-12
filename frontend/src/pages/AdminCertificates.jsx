import { useEffect, useState } from "react";
import api, { API_URL } from "../services/api";

export default function AdminCertificates() {
  const [items, setItems] = useState([]);

  const load = async () => {
    try {
      const res = await api.get("/admin/certificates");
      setItems(res.data);
    } catch (err) {
      console.error("Ошибка загрузки сертификатов", err);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const openPdf = (url) => {
    window.open(`${API_URL}${url}`, "_blank");
  };

  const downloadPdf = (url) => {
    window.location.href = `${API_URL}${url}`;
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Реестр сертификатов</h2>

      <table className="table table-bordered table-hover">
        <thead className="table-light">
          <tr>
            <th>ID</th>
            <th>ФИО</th>
            <th>Email</th>
            <th>Курс</th>
            <th>Дата</th>
            <th>Проверка</th>
            <th>PDF</th>
          </tr>
        </thead>

        <tbody>
          {items.length === 0 && (
            <tr>
              <td colSpan="7" className="text-center py-3">
                Нет сертификатов
              </td>
            </tr>
          )}

          {items.map((c) => (
            <tr key={c.id}>
              <td>{c.id}</td>
              <td>{c.fullname}</td>
              <td>{c.email}</td>
              <td>{c.course}</td>
              <td>{c.date}</td>
              <td>
                <a
                  href={`/verify/${c.public_token}`}
                  target="_blank"
                  className="btn btn-outline-primary btn-sm"
                >
                  Проверить
                </a>
              </td>
              <td>
                <button
                  onClick={() => openPdf(c.pdf_url)}
                  className="btn btn-primary btn-sm me-2"
                >
                  Открыть
                </button>
                <button
                  onClick={() => downloadPdf(c.pdf_url)}
                  className="btn btn-secondary btn-sm"
                >
                  Скачать
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

