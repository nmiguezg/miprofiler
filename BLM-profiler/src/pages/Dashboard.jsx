import { useEffect, useState } from "react";
import data from "/src/coll.json";
// import BarChart from "../components/MyBarChart/BarChart";
import PieChart from "../components/Charts/PieChart";
import BarChart from "../components/Charts/BarChart";


export default function Dashboard() {
  const [[acumAge, acumGender], setState] = useState([{}, {}]);
  useEffect(() => {
    let acumGender = {};
    let acumAge = {};

    data.categories.gender.forEach(category => {
      acumGender[category] = 0;
    });
    data.categories.age.forEach(category => {
      acumAge[category] = 0;
    });
    const newState = data.Users.reduce(([acumAge, acumGender], currentValue) => {
      acumAge[currentValue.age]++;
      acumGender[currentValue.gender]++;
      return [acumAge, acumGender];
    }, [acumAge, acumGender]);
    setState(newState);
  }, []);
  return (
    <>
      <h2>Dashboard</h2>
      <h3>Edad</h3>
      <main className="dashboard">
        <div >
          <BarChart data={acumAge} title={'Género'} />
        </div>
        <div className="pie-chart" >
          <PieChart data={acumAge} title={'Género'} />
        </div>
      </main>
      <h3>Género</h3>
      <main className="dashboard">
        <div >
          <BarChart data={acumGender} title={'Género'} />
        </div>
        <div className="pie-chart" >
          <PieChart data={acumGender} title={'Género'} />
        </div>
      </main>
    </>
  );
}
