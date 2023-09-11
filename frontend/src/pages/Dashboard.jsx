import PieChart from "../components/Charts/PieChart";
import BarChart from "../components/Charts/BarChart";
import ProfileService from "../services/ProfileService";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import "./Dashboard.css";

export default function Dashboard() {
  const [edad, setEdad] = useState(false);
  function handleClick() {
    setEdad(!edad);
  }
  // function exportCollection() {
  //   const element = document.createElement("a");
  //   const file = new Blob([JSON.stringify(coll)], { type: 'json' });
  //   element.href = URL.createObjectURL(file);
  //   element.download = "collection.json";
  //   document.body.appendChild(element); // Required for this to work in FireFox
  //   element.click();
  // }
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
  return (
    <div className="content">
      <h1>Dashboard</h1>
      {coll ?
        <>
          <main>
            <div className="buttons">
              <button onClick={handleClick}>Edad</button> <button onClick={handleClick}>Género</button>
            </div>
            {!edad && <div className="dashboard">
              <div >
                <BarChart data={coll['grupos']['edad']} />
              </div>
              <div>
                <PieChart data={coll['grupos']['edad']} />
              </div>
            </div>}

            {edad && <div className="dashboard">
              <div>
                <BarChart data={coll['grupos']['genero']} />
              </div>
              <div>
                <PieChart data={coll['grupos']['genero']} />
              </div>
            </div>}

          </main>
          {/* <aside>
            <button className="export" onClick={exportCollection}>Export</button>
          </aside> */}
        </>
        : (
          <>
            <p>Todavía no hay usuarios perfilados, perfila una colección para poder ver sus estadísticas.</p>
            <Link to="/">Volver</Link>
          </>)}
    </div>
  );
}
