import "./App.css"
import { Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";

export default function App() {

  return (
    <>
      <Title />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
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
      </nav>
    </header>);
}

