import React from 'react';
import Chart from 'chart.js/auto';
import { Bar } from 'react-chartjs-2';

function getColor(i) {
    const backgroundColor = [
        'rgba(44, 39, 245, 0.8)',
        'rgba(214, 19, 144, 0.8)',
        // 'rgba(255, 205, 86, 0.5)',
        // 'rgba(75, 192, 192, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(153, 102, 255, 0.5)',
        'rgba(201, 203, 207, 0.5)'
    ]
    const borderColor = [
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

export default function PieChart({ data, title }) {
    const categories = Object.keys(data)
    const values = Object.values(data)
    const conf = {
        labels: categories,
        datasets: [
            {
                label: 'Usuarios',
                data: values,
                backgroundColor: 'rgba(255, 251, 3, 0.8)',
                borderColor: 'rgba(75,192,192,1)',
                borderWidth: 1,
            },

        ],
    };
    const options = {
        scales: {
            x: {
                grid: {
                    color: 'rgba(255,255,255,0.1)',
                },
            },
            y: {
                grid: {
                    color: 'rgba(255,255,255,0.1)',
                },
            },
        },
        responsive: true,
    }
    return <Bar data={conf} style={{ width: "400px", height: "200px"}} options={options} />;
}