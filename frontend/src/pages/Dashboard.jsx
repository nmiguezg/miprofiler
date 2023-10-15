import PieChart from "@/components/Charts/PieChart";
import BarChart from "@/components/Charts/BarChart";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import styles from "./styles/dashboard.module.css";
import UsersTable from "@/components/UsersTable/UsersTable"
import InfoCard from "@/components/Cards/InfoCard";
import DropDownButton from "@/components/Utils/DropDownButton";
import ProfilerService from "@/services/ProfilerService";

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
        <InfoCard title="Usuarios" data={coll.users.totalUsers} />
        <InfoCard title="Tiempo de perfilado" data={Number.parseFloat(coll.time).toFixed(3)} />
        <InfoCard title="Algoritmo" data={coll.algorithm} />
        <InfoCard className={styles.card} title="Colección" data={coll.name} />
        <div className={styles.card}>
          <p>Filtros</p>
          <p>Edad: {filters.age &&
            filters.age && <ClearButton action={() => setFilters({ ...filters, age: undefined })} />} </p>
          <p>Género: {filters.gender &&
            filters.gender && <ClearButton action={() => setFilters({ ...filters, gender: undefined })} />} </p>

        </div>
        <div>
          <DropDownButton name="Edad"
            options={Object.keys(coll.users.age)}
            handleSelection={(category) => { setFilters({ ...filters, age: category }) }}
          />
          <DropDownButton name="Género"
            options={Object.keys(coll.users.gender)}
            handleSelection={(category) => { setFilters({ ...filters, gender: category }) }}
          />
        </div>


      </div>
      <div className={styles.charts}>
        <UsersTable collId={collId} filters={filters}></UsersTable>
        <div className={styles.chart}>
          <h2>Edad</h2>
          <BarChart
            data={usersStats['age']}
            filters={filters}
            setFilters={setFilters}
          />
        </div>
        <div className={styles.chart}>
          <h2>Género</h2>
          <PieChart
            data={usersStats['gender']}
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
function ClearButton({ action }) {
  return (
    <svg onClick={action} style={{ cursor: "pointer", color: "red" }} xmlns="http://www.w3.org/2000/svg" height="30" viewBox="0 0 24 24" width="30"><path d="M0 0h24v24H0z" fill="none" /><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" /></svg>

  )
}