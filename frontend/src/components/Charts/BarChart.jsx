import plugin from "chartjs-plugin-datalabels";
import {
    Chart,
    Colors,
    BarController,
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
} from 'chart.js'

Chart.register(
    Colors,
    BarController,
    BarElement,
    CategoryScale,
    LinearScale,
    plugin,
    Tooltip,
);
import { Bar } from 'react-chartjs-2';


const options = {
    scales: {
        x: {
            ticks: {
                color: 'rgba(255,255,255,0.8)',
                font: {
                    weight: "400",
                },
            },
            grid: {
                color: 'rgba(255,255,255,0.15)',
            },
        },
        y: {
            ticks: {
                color: 'rgba(255,255,255,0.8)',
                font: {
                    weight: "400",
                },
            },
            grid: {
                color: 'rgba(255,255,255,0.15)',
            },
        },
    },
    plugins: {
        legend: {
            display: false,
        },
        datalabels: {
            align: "end",
            anchor: "middle",
            font: { weight: 550 },
            color: 'rgba(255,255,255, 1)',
        },
        tooltip: {
            backgroundColor: "rgba(12, 16, 59, 1)",
            displayColors: true,
            titleColor: "#E3E6EF",
            bodyColor: "#E3E6EF",
            padding: 12,
            titleFont: {
                size: 11 + 1,
                weight: "bold",
            },
            bodyFont: {
                size: 11,
            },
        },
    },
    borderColor: 'white',
    mantainAspectRatio: false,
    aspectRatio: 4 / 4,
    responsive: true,
    elements: {
        bar: {
            borderRadius: 0,
        },
    },
    datasets: {
        bar: {
            barThickness: 35,
        },
    },
    minBarLength: 1,
    inflateAmount: 'auto',
}

import PropTypes from 'prop-types';

export default function PieChart({ data, filters, setFilters }) {

    const categories = Object.keys(data)
    const values = Object.values(data)
    const conf = {
        labels: categories,
        datasets: [
            {
                label: 'Usuarios',
                data: values,
                backgroundColor: 'rgba(227, 248, 0, 0.67)',
                borderColor: 'rgba(75,192,192,1)',
                borderWidth: 1,
            },

        ],
    };
    const barChartOptions = {
        ...options, onClick:
            (event, elements) => {
                if (elements.length > 0
                    && filters.age !== categories[elements[0].index]) {
                    setFilters({ ...filters, age: categories[elements[0].index] });
                }
            }
    }
    return <Bar data={conf} options={barChartOptions} />;
}
PieChart.propTypes = {
    data: PropTypes.object.isRequired,
    setFilters: PropTypes.func.isRequired,
    filters: PropTypes.object.isRequired,
};