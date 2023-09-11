import "./App.css"
import { Link, Route, Routes, useNavigate } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import ErrorPage from "./error-page";
import Users from "./pages/Users";
import User from "./pages/User";
import Login from "./pages/Login";

export default function App() {

  return (
    <>
      <Title />
      <div className="container">
        <Routes>
          <Route path="/auth" element={<Login />} />
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/users" element={<Users />} />
          <Route path="/*" element={<ErrorPage />} />
          <Route path="/users/:id" element={<User />} />
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
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/users">Usuarios</Link></li>
      </div>
    </nav>
  );
}

