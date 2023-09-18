import "./App.css"
import { Link, Route, Routes, useNavigate } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import ErrorPage from "./pages/error-page";
import User from "./pages/User";

export default function App() {

  return (
    <>
      <Title />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/*" element={<ErrorPage />} />
          <Route path="/users/:id" element={<User />} />
        </Routes>
      </div>
    </>)
}

function Title() {
  const navigate = useNavigate();
  const results = sessionStorage.getItem('coll') !== null;
  return (
    <nav className="navbar">
      <span className="logo" onClick={()=>{return navigate("/")}}>BLM Profiler</span>
      <div className="nav">

        { results && <li><Link to="/dashboard">Resultados</Link></li>}
      </div>
    </nav>
  );
}

