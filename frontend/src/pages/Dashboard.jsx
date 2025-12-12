import { useContext } from "react";
import { AuthContext } from "../auth/AuthContext";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const { user, logout } = useContext(AuthContext);

  if (!user?.token) {
    window.location.href = "/login";
    return null;
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3>Дашборд</h3>
          <p className="text-muted mb-0">
            Привет, <strong>{user.fullname}</strong> ({user.role})
          </p>
        </div>
        <button className="btn btn-outline-danger btn-sm" onClick={logout}>
          Выйти
        </button>
      </div>

      {user.role === "operator" && (
        <div className="row g-3">
          <div className="col-md-4">
            <div className="card shadow-sm">
              <div className="card-body">
                <h5 className="card-title">Студенты</h5>
                <p className="card-text">Просмотр и добавление студентов.</p>
                <Link to="/operator/students" className="btn btn-primary btn-sm">
                  Открыть
                </Link>
              </div>
            </div>
          </div>

          <div className="col-md-4">
            <div className="card shadow-sm">
              <div className="card-body">
                <h5 className="card-title">Результаты экзаменов</h5>
                <p className="card-text">Отметить сдачу курса студентом.</p>
                <Link to="/operator/exam-record" className="btn btn-primary btn-sm">
                  Открыть
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {user.role === "admin" && (
        <div className="row g-3">
          <div className="col-md-4">
            <div className="card shadow-sm">
              <div className="card-body">
                <h5 className="card-title">Заявки на утверждение</h5>
                <p className="card-text">Результаты от операторов.</p>
                <Link to="/admin/approvals" className="btn btn-primary btn-sm">
                  Открыть
                </Link>
              </div>
            </div>
          </div>

          <div className="col-md-4">
            <div className="card shadow-sm">
              <div className="card-body">
                <h5 className="card-title">Сертификаты</h5>
                <p className="card-text">Реестр выданных сертификатов.</p>
                <Link
                  to="/admin/certificates"
                  className="btn btn-primary btn-sm"
                >
                  Открыть
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {user.role !== "operator" && user.role !== "admin" && (
        <p>Для этой роли пока нет интерфейса.</p>
      )}
    </div>
  );
}

