import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import ProfilerService from '../services/ProfilerService';
import styles from './styles/collections.module.css';

export default function Collections() {
  const [collections, setCollections] = useState([]);
  const navigate = useNavigate();
  useEffect(() => {
    ProfilerService.findCollections().then((data) => {
      setCollections(data);
    });
  }, []);

  function handleNavigation(collection) {
    if (window.innerWidth < 550) {
      navigate(`/collections/${collection.id}`, { state: collection });
    }
  }
  return (
    <div className={styles.content}>
      <h1 className={styles.title}>Colecciones</h1>
      <div className={styles.scroll}>
        <table className={styles.table}>
          <thead className={styles.thead}>
            <tr className={styles.trh}>
              <th>Fichero</th>
              <th>Algoritmo</th>
              <th>Fecha</th>
              <th className={styles.prescindible}>Usuarios</th>
              <th className={styles.prescindible_link}>Acciones</th>
            </tr>
          </thead>
          <tbody className={styles.tbody}>
            {collections.map((collection) => (
              <tr
                className={styles.tr}
                key={collection.id}
                onClick={() => handleNavigation(collection)}
              >
                <td>{collection.name}</td>
                <td>{collection.algorithm}</td>
                <td>{new Date(collection.timestamp * 1000)
                  .toLocaleString(
                    'es-ES', { day: 'numeric', month: 'numeric', year: 'numeric' }
                  )
                }
                </td>
                <td className={styles.prescindible}>
                  {collection.users.totalUsers}</td>
                <td className={styles.prescindible_link}>
                  <Link
                    to={`/collections/${collection.id}`}
                    state={collection}
                  >Ver</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}