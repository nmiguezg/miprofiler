import { useState } from "react";

export default function Home() {
  const [profiling, setProfiling] = useState(false);
  function handleSubmit() {
    event.preventDefault();
    setProfiling(true);
    // const form = event.target
    setProfiling(false);
  }
  const spinner = profiling ? "spinner" : "spinner hidden";
  return (
    <>
      <h2>Perfilar colección</h2>
      <form id="profiler-form" encType="multipart/form-data" onSubmit={handleSubmit}>
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
