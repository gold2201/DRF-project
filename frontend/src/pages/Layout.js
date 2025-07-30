import './pagesStyle/Layout.css';
import { Outlet, Link } from 'react-router-dom';

export default function Layout() {
  return (
    <div className="page-container">
      <header className="header">
        <h1 className="site-title">MarketConnect</h1>
        <nav className="nav">
          <Link to="/" className="nav-button">Главная</Link>
          <Link to="/shops" className="nav-button">Магазины</Link>
          <Link to="/about" className="nav-button">О проекте</Link>
          <Link to="/login" className="nav-button">Вход</Link>
          <Link to="/register" className="nav-button">Регистрация</Link>
          <Link to="/private" className="nav-button">Приватный магазин</Link>
        </nav>
      </header>

      <main className="main-content">
        <Outlet />
      </main>

      <footer className="footer">
        <p className="footer-text">© 2025 MarketConnect. Все права защищены.</p>
        <div className="footer-links">
          <a href="https://github.com/gold2201" target="_blank" rel="noopener noreferrer" className="footer-link">GitHub</a>
          <a href="https://linkedin.com/in/" target="_blank" rel="noopener noreferrer" className="footer-link">LinkedIn</a>
        </div>
      </footer>
    </div>
  );
}
