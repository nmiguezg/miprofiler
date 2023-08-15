import { useEffect, useRef, useState } from "react";
import "./App.css"
import * as d3 from "d3"
import data from "../public/coll.json"
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
  const main = useRef()
  useEffect(() => {
    // Datos de ejemplo
    const [acumAge, acumGender] = data.Users.reduce(([acumAge, acumGender], currentValue) => {
      if (!(currentValue.age in acumAge)){
        acumAge[currentValue.age]=0
      }
      if (!(currentValue.gender in acumGender)){
        acumGender[currentValue.gender]=0
      }
      acumAge[currentValue.age]++
      acumGender[currentValue.gender]++
      return [acumAge, acumGender]
    }, [{},{}]);

    // Tamaño del gráfico
    var width = 200;
    var height = 300;

    // Crear el contenedor SVG
    var svg = main.current
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    // // Escala de ejes
    // var xScale = d3.scaleBand()
    //   .domain(data.map(d => d.categoria))
    //   .range([0, width])
    //   .padding(0.1);

    // var yScale = d3.scaleLinear()
    //   .domain([0, d3.max(data, d => d.valor)])
    //   .range([height, 0]);

    // // Crear las barras
    // svg.selectAll("rect")
    //   .data(data)
    //   .enter()
    //   .append("rect")
    //   .attr("x", d => xScale(d.categoria))
    //   .attr("y", d => yScale(d.valor))
    //   .attr("width", xScale.bandwidth())
    //   .attr("height", d => height - yScale(d.valor))
    //   .attr("fill", "steelblue");

    // // Agregar ejes
    // svg.append("g")
    //   .attr("transform", "translate(0," + height + ")")
    //   .call(d3.axisBottom(xScale));

    // svg.append("g")
    //   .call(d3.axisLeft(yScale));
  }, [])
  return (
    <main ref={main}>
      Dashboard
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

