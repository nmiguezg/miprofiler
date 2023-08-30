import "./App.css"
import { Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import ErrorPage from "./error-page";
import Users from "./pages/Users";

export default function App() {

  return (
    <>
      <Title />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/collection" element={<Users />} />
        <Route path="/*" element={<ErrorPage />} />

      </Routes>
    </>)
}

function Title() {
  return (
    <header className="header">
      <h1>BLM Profiler</h1>
      <nav className="nav">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/collection">View users</Link></li>
      </nav>
    </header>);
}

