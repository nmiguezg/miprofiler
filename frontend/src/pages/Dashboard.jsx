// import BarChart from "../components/MyBarChart/BarChart";
import PieChart from "../components/Charts/PieChart";
import BarChart from "../components/Charts/BarChart";
import { Link } from "react-router-dom";



export default function Dashboard() {
  const coll = JSON.parse(sessionStorage.getItem('coll'))


  return (
    <>
      <h2>Dashboard</h2>
      {coll ?
        <main>
          <h3>Edad</h3>

          <div className="dashboard">
            <div >
              <BarChart data={coll['grupos']['edad']} />
            </div>
            <div>
              <PieChart data={coll['grupos']['edad']} />
            </div>
          </div>
          <h3>Género</h3>
          <div className="dashboard">
            <div>
              <BarChart data={coll['grupos']['genero']} />
            </div>
            <div>
              <PieChart data={coll['grupos']['genero']} />
            </div>
          </div>
        </main>
        : (
          <>
            <p>Todavía no hay usuarios perfilados, perfila una colección para poder ver sus estadísticas.</p>
            <Link to="/">Volver</Link>
          </>)}
    </>
  );
}
