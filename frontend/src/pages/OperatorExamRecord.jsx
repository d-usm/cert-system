import { useEffect, useState } from "react";
import api from "../services/api";

export default function OperatorExamRecord() {
  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [studentId, setStudentId] = useState("");
  const [courseId, setCourseId] = useState("");
  const [isPassed, setIsPassed] = useState("true");

  useEffect(() => {
    api.get("/operator/students").then((res) => setStudents(res.data));
    api.get("/courses/").then((res) => setCourses(res.data));
  }, []);

  const submit = async () => {
    if (!studentId || !courseId) {
      alert("Выбери студента и курс");
      return;
    }

    try {
      await api.post("/exams/record", {
        student_id: Number(studentId),
        course_id: Number(courseId),
        is_passed: isPassed === "true",
      });
      alert("Результат отправлен на утверждение");
    } catch (err) {
      console.error(err);
      alert("Ошибка при сохранении результата");
    }
  };

  return (
    <div className="container mt-4">
      <h3 className="mb-3">Отметить сдачу курса</h3>

      <div className="mb-3">
        <label className="form-label">Студент</label>
        <select
          className="form-select"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
        >
          <option value="">Выберите студента</option>
          {students.map((s) => (
            <option key={s.id} value={s.id}>
              {s.fullname} ({s.email})
            </option>
          ))}
        </select>
      </div>

      <div className="mb-3">
        <label className="form-label">Курс</label>
        <select
          className="form-select"
          value={courseId}
          onChange={(e) => setCourseId(e.target.value)}
        >
          <option value="">Выберите курс</option>
          {courses.map((c) => (
            <option key={c.id} value={c.id}>
              {c.title}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-3">
        <label className="form-label">Статус сдачи</label>
        <select
          className="form-select"
          value={isPassed}
          onChange={(e) => setIsPassed(e.target.value)}
        >
          <option value="true">Сдал</option>
          <option value="false">Не сдал</option>
        </select>
      </div>

      <button className="btn btn-primary" onClick={submit}>
        Отправить на утверждение
      </button>
    </div>
  );
}

