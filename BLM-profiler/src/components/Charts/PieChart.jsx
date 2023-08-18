import React from 'react';
import {
    Chart,
    Colors,
    ArcElement,
    PieController,
    Legend,
    Tooltip
  } from 'chart.js'
  
  Chart.register(
    Colors,
    ArcElement,
    PieController,
    Legend,
    Tooltip,
  );
import { Pie } from 'react-chartjs-2';

function getColor(i) {
    const backgroundColor= [
        'rgba(44, 39, 245, 0.8)',
        'rgba(214, 19, 144, 0.8)',
        // 'rgba(255, 205, 86, 0.5)',
        // 'rgba(75, 192, 192, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(153, 102, 255, 0.5)',
        'rgba(201, 203, 207, 0.5)'
      ]
      const borderColor= [
        'rgb(255, 99, 132)',
        'rgb(255, 159, 64)',
        'rgb(255, 205, 86)',
        'rgb(75, 192, 192)',
        'rgb(54, 162, 235)',
        'rgb(153, 102, 255)',
        'rgb(201, 203, 207)'
      ]
    return backgroundColor[i];
}

export default function PieChart({ data }) {
    const categories = Object.keys(data)
    const values = Object.values(data)
    const colors = categories.map((_,index) => getColor(index))

    const conf = {
        labels: categories,
        datasets: [
            {
                label: 'Usuarios',
                data: values,
                backgroundColor: colors,
                borderColor: 'rgba(75,192,192,1)',
                borderWidth: 1,
            },

        ],
    };
    const options = {
        responsive: true,
        mantainAspectRatio: false,
    }
    return <Pie data={conf} options={options}/>;
}