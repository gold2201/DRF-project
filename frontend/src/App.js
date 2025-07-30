import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './pages/Layout';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import PublicShopsPage from './pages/PublicShopsPage';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="about" element={<AboutPage />} />
          <Route path="shops" element={<PublicShopsPage />} />
          {/* Заглушки */}
          <Route path="login" element={<p>Страница входа (будет позже)</p>} />
          <Route path="register" element={<p>Регистрация (будет позже)</p>} />
          <Route path="private" element={<p>Приватный магазин (будет позже)</p>} />
          <Route path="*" element={<p>404 — Страница не найдена</p>} />
        </Route>
      </Routes>
    </Router>
  );
}


