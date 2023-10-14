import "./App.css"
import { Link, Route, Routes, useNavigate } from "react-router-dom";
import Collections from './pages/Collections';
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
          <Route path="/collections" element={<Collections />} />
          <Route path="/collections/:id" element={<Dashboard />} />
          <Route path="/*" element={<ErrorPage />} />
          <Route path="/collections/:id/users/:id" element={<User />} />
        </Routes>
      </div>
    </>)
}

function Title() {
  const navigate = useNavigate();
  return (
    <nav className="navbar">
      <span className="logo" onClick={()=>{return navigate("/")}}>BLM Profiler</span>
      <div className="nav">
        <li><Link to="/collections">Colecciones</Link></li>
      </div>
    </nav>
  );
}

