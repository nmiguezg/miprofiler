import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import ProfilerService from '../services/ProfilerService';

export default function Collections() {
  const [collections, setCollections] = useState([]);

  useEffect(() => {
    ProfilerService.findCollections().then((data) => {
        setCollections(data);
        console.log(data);
        });
    }, []);

  return (
    <div>
      <h1>Collections</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {collections.map((collection) => (
            <tr key={collection.id}>
              <td>{collection.name}</td>
              <td>{collection.algorithm}</td>
              <td>
                <Link to={`/collections/${collection.id}`}>View</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}