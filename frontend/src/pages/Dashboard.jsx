import PieChart from "@/components/Charts/PieChart";
import BarChart from "@/components/Charts/BarChart";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import styles from "./styles/dashboard.module.css";
import UsersTable from "@/components/UsersTable/UsersTable"
import ProfilerService from "../services/ProfilerService";

export default function Dashboard() {
  const collId = useLocation().pathname.split('/')[2];
  const [coll, setColl] = useState(JSON.parse(sessionStorage.getItem('coll')));
  useEffect(() => {
    console.log(collId);

    if (coll == null) {
      const collection = JSON.parse(sessionStorage.getItem('coll'));
      if (collection != null && collId === collection.id) {
        setColl(collection);
        return;
      }
      ProfilerService.getCollectionById(collId)
        .then((data) => {
          console.log(data);
          setColl(data);
          sessionStorage.setItem('coll', JSON.stringify(data));
        }).catch((error) => {
          console.log(error);
        });
    }
  }, []);
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
          <p>Tiempo</p>
          <h2>{coll.time}</h2>
        </div>
        <div className={styles.card}>
          <p>Algoritmo</p>
          <h2>Modaresi</h2>
        </div>
        <div className={styles.card}>
          <p>Colección</p>
          <h2>{coll.name}</h2>
        </div>
      </div>
      <div className={styles.charts}>
        <UsersTable></UsersTable>
        <div className={styles.card + " " + styles.chart}>
          <h2>Edad</h2>
          <BarChart data={coll['users']['age']} />
        </div>
        <div className={styles.card + " " + styles.chart}>
          <h2>Género</h2>
          <PieChart data={coll['users']['gender']} />
        </div>
      </div>
      {/* <aside>
    <button className="export" onClick={exportCollection}>Export</button>
  </aside> */}
    </div>
  );
}
