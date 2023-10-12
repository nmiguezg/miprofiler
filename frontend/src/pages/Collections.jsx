import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import ProfilerService from '../services/ProfilerService';

export default function Collections() {
  const [collections, setCollections] = useState([]);

  useEffect(() => {
    ProfilerService.findCollections().then((data) => {
      setCollections(data);
    });
  }, []);

  return (
    <div>
      <h1>Collections</h1>
      <table>
        <thead>
          <tr>
            <th>Fichero</th>
            <th>Algoritmo</th>
            <th>Fecha</th>
            <th>Usuarios</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {collections.map((collection) => (
            <tr key={collection.id}>
              <td>{collection.name}</td>
              <td>{collection.algorithm}</td>
              <td>{new Date(collection.timestamp * 1000).toLocaleString()}</td>
              <td>{collection.users.totalUsers}</td>
              <td>
                <Link
                  to={`/collections/${collection.id}`}
                  state={collection}
                >View</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}