import PieChart from "@/components/Charts/PieChart";
import BarChart from "@/components/Charts/BarChart";
import ProfileService from "@/services/ProfileService";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import styles from "./styles/dashboard.module.css";
import UsersTable from "@/components/UsersTable/UsersTable"

export default function Dashboard() {
  function exportCollection() {
    const element = document.createElement("a");
    const file = new Blob([JSON.stringify(coll)], { type: 'json' });
    element.href = URL.createObjectURL(file);
    element.download = "collection.json";
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  }
  const [coll, setColl] = useState(JSON.parse(sessionStorage.getItem('coll')));
  useEffect(() => {
    if (coll == null) {
      ProfileService.getUsers(0, 0).then((data) => {
        if (data == null) {
          return;
        }
        setColl(data);
        sessionStorage.setItem('coll', JSON.stringify(data));
      });
    }
  }, []);
  if (coll == null) {
    return (
      <>
        <p>Todavía no hay usuarios perfilados, perfila una colección para poder ver sus estadísticas.</p>
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
          <h2>BLM.csv</h2>
        </div>
      </div>
      <div className={styles.charts}>
        <UsersTable></UsersTable>
        <div className={styles.card + " " + styles.chart}>
          <h2>Edad</h2>
          <BarChart data={coll['users']['edad']} />
        </div>
        <div className={styles.card + " " + styles.chart}>
          <h2>Género</h2>
          <PieChart data={coll['grupos']['genero']} />
        </div>
      </div>
      {/* <aside>
    <button className="export" onClick={exportCollection}>Export</button>
  </aside> */}
    </div>
  );
}
