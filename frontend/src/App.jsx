import "./App.css"
import { Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import ErrorPage from "./error-page";
import Users from "./pages/Users";
import User from "./pages/User";

export default function App() {

  return (
    <>
      <Title />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/collection" element={<Users />} />
          <Route path="/*" element={<ErrorPage />} />
          <Route path="/collection/:id" element={<User />} />
        </Routes>
      </div>
    </>)
}

function Title() {
  return (
    <navbar className="header">
      <span className="logo">BLM Profiler</span>
      <nav className="nav">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/collection">View users</Link></li>
      </nav>
    </navbar>
  );
}

