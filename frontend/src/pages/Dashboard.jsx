import PieChart from "@/components/Charts/PieChart";
import BarChart from "@/components/Charts/BarChart";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import styles from "./styles/dashboard.module.css";
import UsersTable from "@/components/UsersTable/UsersTable"
import ProfilerService from "../services/ProfilerService";

export default function Dashboard() {
  const location = useLocation();
  const collId = location.pathname.split('/')[2];
  const [coll, setColl] = useState(location.state);
  const [filters, setFilters] = useState({});
  const [usersStats, setUsersStats] = useState(location.state.users);

  useEffect(() => {
    if (location.state == null && filters == null) {
      ProfilerService.getCollectionById(collId)
        .then((data) => {
          setColl(data);
          setUsersStats(data.users);
        }).catch((error) => {
          console.log(error);
        });
    } else if (filters != null) {
      ProfilerService.getUsersStats(collId, filters)
        .then((data) => {
          setUsersStats(data);
        }).catch((error) => {
          console.log(error);
        });
    }
  }, [collId, filters, location.state]);
  function handleChartClick(event, elements) {
    if (elements.length > 0) {
      const category = elements[0]._model.label;
      const filteredUsers = coll.users.filter((user) => user.category === category);
      setColl({ ...coll, users: { ...coll.users, filteredUsers } });
    }
  }
  if (coll == null) {
    return (
      <>
        <p>Path no válido, la colección que estás intentando ver no existe. Vuelve para poder perfilar una colección.</p>
        <Link to="/">Volver</Link>
      </>
    )
  }
  return (
    <div className={styles.dashboard}>
      <div className={styles.cards}>
        <div className={styles.card}>
          <p>Usuarios</p>
          <h2>{coll.users.totalUsers}</h2>
        </div>
        <div className={styles.card}>
          <p>Tiempo de perfilado</p>
          <h2>{Number.parseFloat(coll.time).toFixed(3)}</h2>
        </div>
        <div className={styles.card}>
          <p>Algoritmo</p>
          <h2>{coll.algorithm}</h2>
        </div>
        <div className={styles.card}>
          <p>Colección</p>
          <h2>{coll.name}</h2>
        </div>
        <div className={styles.card}>
          <p>Filtros</p>
          {(filters.age || filters.gender) &&
            <>
              <h2>
                {filters.age && 'Edad: ' + filters.age}
                {filters.gender && 'Género: ' + filters.gender}

              </h2>
              <button onClick={() => setFilters({})}>Limpiar</button>
            </>
          }

        </div>

      </div>
      <div className={styles.charts}>
        <UsersTable collId={collId} filters={filters}></UsersTable>
        <div className={styles.card + " " + styles.chart}>
          <h2>Edad</h2>
          <BarChart
            data={filters.gender ? usersStats['age']: coll['users']['age']}
            filters={filters}
            setFilters={setFilters}
          />
        </div>
        <div className={styles.card + " " + styles.chart}>
          <h2>Género</h2>
          <PieChart
            data={filters.age ? usersStats['gender']: coll['users']['gender']}
            filters={filters}
            setFilters={setFilters}
          />
        </div>
      </div>
      {/* <aside>
    <button className="export" onClick={exportCollection}>Export</button>
  </aside> */}
    </div>
  );
}
