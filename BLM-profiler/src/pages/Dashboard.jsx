// import BarChart from "../components/MyBarChart/BarChart";
import PieChart from "../components/Charts/PieChart";
import BarChart from "../components/Charts/BarChart";

export default function Dashboard() {
  const coll = JSON.parse(sessionStorage.getItem('coll'))

  return (
    <>
      <h2>Dashboard</h2>
      {coll ?
      <main>
        <h3>Edad</h3>

        <div className="dashboard">
          <div >
            <BarChart data={coll['grupos']['edad']} />
          </div>
          <div>
            <PieChart data={coll['grupos']['edad']} />
          </div>
        </div>
        <h3>Género</h3>
        <div className="dashboard">
          <div>
            <BarChart data={coll['grupos']['genero']} />
          </div>
          <div>
            <PieChart data={coll['grupos']['genero']} />
          </div>
        </div>
        <h3>Usuarios</h3>
        <Users users={coll['usuarios']} />
      </main>
      : <p>No hay datos para mostrar</p>}
    </>
  );
}
function Users({ users }) {
  return (
    <ul>
      {users.map((user, index) => (
        <li key={index}>
          {user.genero} {user.edad} {user.id}
        </li>
      ))}
    </ul>
  );
}