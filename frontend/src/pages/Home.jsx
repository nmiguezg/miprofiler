import { useState } from "react";
import ProfileService from "../services/ProfileService";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const [profiling, setProfiling] = useState(false);
  const [error, setError] = useState(null);
  const [validFile, setValidFile] = useState(false);
  const [flag, setFlag] = useState(false);
  const navigate = useNavigate();

  function handleSubmit(event) {
    event.preventDefault();
    if (!validFile) {
      return;
    }
    const form = event.target;
    setError(null);
    setProfiling(true);
    form.elements['submit'].disabled = true;
    ProfileService.profileUsers(
      form.elements['file'].files[0],
      form.elements['algoritmo'].value
    ).then((data) => {
      sessionStorage.setItem('coll', JSON.stringify(data));
      navigate("/dashboard");
    }).catch((error) => {
      console.log(error);
      setError(error);
    }).finally(() => {
      setProfiling(false);
      form.elements['submit'].disabled = false;
    });
  }
  function handleFileUpload(event) {
    if (event.target.form.elements['file'].files.length === 0) {
      setFlag(false);
      console.log('no file');
      return
    }
    setFlag(true);
    const form = event.target.form;
    const file = form.elements['file'].files[0];
    const reader = new FileReader();
    reader.readAsText(file);
    reader.onload = function (e) {
      const csv = e.target.result.split('\n');
      const header = csv[0].split(',');
      if (header.includes('label') && header.includes('post')) {
        setValidFile(true);
      } else {
        setValidFile(false);
        console.log('invalid file');
        console.log(flag.current);
      }
    };
  }
  return (
    <div className="content">
      <h1>Perfilar colección</h1>
      <form className="profiler-form" encType="multipart/form-data" onSubmit={handleSubmit}>
        <div className="form-fields">
          <label>
            Archivo a perfilar
            <input type="file" name="file" accept=".csv, .txt" required="True" onChange={handleFileUpload}></input>
          </label>
          <label>
            Algoritmo
            <select name="algoritmo">
              <option value="modaresi">Modaresi</option>
              <option value="grivas">Grivas</option>
            </select>
          </label>
        </div>
        {flag && (validFile ? <div>Archivo válido</div> : <div>Archivo inválido</div>)}
        {profiling && <div id="spinner" className='spinner'></div>}
        <input type="submit" name="submit" className="submit" value="Perfilar"></input>
        {error && <p>Se ha producido un error al perfilar la colección</p>}
      </form>
    </div>
  );
}
