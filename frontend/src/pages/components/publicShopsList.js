import '../pagesStyle/PublicShopListPage.css';
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function PublicShopList() {
  const [shops, setShops] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/api/shops/public-shops/')
      .then(response => setShops(response.data))
      .catch(err => {
        console.error('Ошибка при получении публичных магазинов:', err);
        setError('Не удалось загрузить магазины');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p>{error}</p>;
  if (shops.length === 0) return <p>Магазинов нет</p>;

  return (
    <ul>
      {shops.map(shop => (
        <li key={shop.id}>{shop.name}</li>
      ))}
    </ul>
  );
}
