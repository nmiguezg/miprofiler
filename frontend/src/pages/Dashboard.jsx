import PieChart from "@/components/Charts/PieChart";
import BarChart from "@/components/Charts/BarChart";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import styles from "./styles/dashboard.module.css";
import UsersTable from "@/components/UsersTable/UsersTable"
import InfoCard from "@/components/Cards/InfoCard";
import ProfilerService from "../services/ProfilerService";

export default function Dashboard() {
  const location = useLocation();
  const collId = location.pathname.split('/')[2];
  const [coll, setColl] = useState(location.state);
  const [filters, setFilters] = useState({});
  const [usersStats, setUsersStats] = useState(location.state ? location.state.users : null);
  useEffect(() => {
    if (location.state == null) {
      ProfilerService.getCollectionById(collId)
        .then((data) => {
          setColl(data);
          setUsersStats(data.users);
        }).catch((error) => {
          console.log(error);
        });
    }
  }, [collId, location.state]);

  useEffect(() => {
    ProfilerService.getUsersStats(collId, filters)
      .then((data) => {
        setUsersStats(data);
      }).catch((error) => {
        console.log(error);
      });
  }, [collId, filters]);

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
        <InfoCard title="Número de usuarios" data={coll.users.totalUsers} />
        <InfoCard title="Tiempo de perfilado" data={Number.parseFloat(coll.time).toFixed(3)} />
        <InfoCard title="Algoritmo" data={coll.algorithm} />
        <InfoCard title="Colección" data={coll.name} />
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
            data={filters.gender ? usersStats['age'] : coll['users']['age']}
            filters={filters}
            setFilters={setFilters}
          />
        </div>
        <div className={styles.card + " " + styles.chart}>
          <h2>Género</h2>
          <PieChart
            data={filters.age ? usersStats['gender'] : coll['users']['gender']}
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
