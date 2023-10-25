import PieChart from "@/components/Charts/PieChart";
import BarChart from "@/components/Charts/BarChart";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import styles from "./styles/dashboard.module.css";
import UsersTable from "@/components/UsersTable/UsersTable"
import InfoCard from "@/components/Cards/InfoCard";
import DropDownButton from "@/components/Utils/DropDownButton";
import ProfilerService from "@/services/ProfilerService";
import FilterList from "../components/FilterList/FilterList";
import FilterItem from "../components/FilterList/FilterItem";

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
      <div className={styles['first-row']}>
        <div className={styles['filter-card']}>
          <h2 id="labelDropdowns">
            Filtrar
          </h2>
          <div aria-labelledby="labelDropdowns" className={styles['filters-container']}>

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
        <div className={styles.cards}>
          <InfoCard title="Usuarios" data={coll.users.totalUsers} />
          <InfoCard title="Tiempo de perfilado" data={Number.parseFloat(coll.time).toFixed(3) + " s"} />
          <InfoCard title="Algoritmo" data={coll.algorithm} />
          <InfoCard title="Colección" data={coll.name} />
        </div>
        <FilterList>
          {filters.age &&
            <FilterItem
              name={"edad"}
              value={filters.age}
              action={() => { setFilters({ ...filters, age: undefined }) }}
            />}
          {filters.gender &&
            <FilterItem
              name={"género"}
              value={filters.gender}
              action={() => { setFilters({ ...filters, gender: undefined }) }}
            />}
        </FilterList>
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