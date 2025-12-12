import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";

export default function VerifyCertificate() {
  const { token } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`/verify/${token}`)
      .then(res => {
        setData(res.data);
        setLoading(false);
      })
      .catch(() => {
        setData({ valid: false });
        setLoading(false);
      });
  }, [token]);

  if (loading) return <div className="container mt-5">Проверяем сертификат…</div>;

  if (!data.valid) {
    return (
      <div className="container mt-5">
        <h2 className="text-danger">❌ Сертификат недействителен</h2>
        <p>Проверьте правильность ссылки или обратитесь в учебный центр.</p>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <h2 className="text-success">✔ Сертификат действителен</h2>

      <div className="mt-4 card p-4 shadow-sm" style={{ maxWidth: "500px" }}>
        <p><b>ФИО:</b> {data.fullname}</p>
        <p><b>Курс:</b> {data.course}</p>
        <p><b>Дата выдачи:</b> {data.date}</p>

        <a className="btn btn-primary mt-3" href={data.pdf_url} target="_blank">
          Скачать PDF
        </a>
      </div>
    </div>
  );
}

