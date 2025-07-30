import './pagesStyle/PublicShopPage.css';
import PublicShopList from "./components/publicShopsList";

export default function PublicShopsPage() {
  return (
    <div className="section-content">
      <h2 className="section-title">Публичные магазины</h2>
      <PublicShopList />
    </div>
  );
}
