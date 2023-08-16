import { useEffect, useState } from "react";
import "./App.css"
import data from "/src/coll.json"
import BarChart from "./components/BarChart";
export default function App() {
  const [dashboard, setDashboard] = useState(true)

  return (
    <>
      <Title />
      {dashboard
        ? <Dashboard setDashboard={setDashboard} />
        : <Form setDashboard={setDashboard} />}
    </>)
}

function Title() {
  return <header>
    <h1>BLM Profiler</h1>
  </header>;
}
function Dashboard({ setDashboard }) {
  const [[acumAge, acumGender], setState] = useState([{}, {}])
  useEffect(() => {
    // Datos de ejemplo
    const newState = data.Users.reduce(([acumAge, acumGender], currentValue) => {
      if (!(currentValue.age in acumAge)) {
        acumAge[currentValue.age] = 0
      }
      if (!(currentValue.gender in acumGender)) {
        acumGender[currentValue.gender] = 0
      }
      acumAge[currentValue.age]++
      acumGender[currentValue.gender]++
      return [acumAge, acumGender]
    }, [{}, {}]);
    setState(newState)
  }, [])
  return (
    <main >
      <BarChart width="300" height="300" data={(acumAge)} />
      <BarChart width="300" height="200" data={(acumGender)} />
    </main>)
}

function Form({ setDashboard }) {
  const [profiling, setProfiling] = useState(false)
  function handleSubmit() {
    event.preventDefault();
    setProfiling(true);
    const form = event.target

    setProfiling(false);
    setDashboard(true)
  }
  const spinner = profiling ? "spinner" : "spinner hidden"
  return (
    <>
      <h2>Perfilar colección</h2>
      <form id="profiler-form" enctype="multipart/form-data" onSubmit={handleSubmit}>
        <label>
          Archivo a perfilar
          <input type="file" name="file" accept=".csv, .txt" required="True"></input>
        </label>
        <label>
          Algoritmo
          <select name="algoritmo">
            <option value="modaresi">Modaresi</option>
            <option value="grivas">Grivas</option>
          </select>
        </label>
        <div id="spinner" className={spinner}></div>
        <input type="submit" value="Perfilar"></input>
      </form>
    </>);
}

