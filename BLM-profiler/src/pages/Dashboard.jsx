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
      <main className="dashboard">
        {/* <BarChart width="300" height="300" data={(acumAge)} /> */}
        {/* <BarChart width="300" height="200" data={(acumGender)} /> */}
        {/* <PieChart data={acumAge}/> */}
        <h3>Edad</h3>
        <div >
          <BarChart data={acumAge} title={'Género'} />
        </div>
        <div className="pie-chart" >
          <PieChart data={acumAge} title={'Género'} />
        </div>
        
        <h3>Género</h3>
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
