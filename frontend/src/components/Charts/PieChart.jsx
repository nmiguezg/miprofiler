import {
    Chart,
    Colors,
    ArcElement,
    PieController,
    Legend,
    Tooltip
} from 'chart.js'
import PropTypes from 'prop-types';

Chart.register(
    Colors,
    ArcElement,
    PieController,
    Legend,
    Tooltip,
);
import { Pie } from 'react-chartjs-2';

const backgroundColor = [
    'rgba(59, 36, 255, 0.94)',
    'rgba(255, 0, 89, 0.94)',
    'rgba(75, 192, 192, 0.5)',
    // 'rgba(54, 162, 235, 0.5)',
    'rgba(153, 102, 255, 0.5)',
    'rgba(201, 203, 207, 0.5)'
]
const options = {
    plugins: {
        legend: {
            labels: {
                boxWidth: 20,
                color: "#E3E6EF",
                font: {
                    size: 11,
                    weight: 300,
                },
            },
        },
        datalabels: {
            align: "middle",
            anchor: "middle",
            font: { weight: '550' },
            color: 'rgba(255,255,255, 1)',
        },
        tooltip: {
            backgroundColor: "rgba(12, 16, 59, 1)",
            displayColors: true,
            titleColor: "#E3E6EF",
            bodyColor: "#E3E6EF",
            padding: 11 + 1,
            titleFont: {
                size: 11 + 1,
                weight: "bold",
            },
            bodyFont: {
                size: 11,
            },
        },
    },
};


export default function PieChart({ data, filters, setFilters }) {
    const categories = Object.keys(data)
    const values = Object.values(data)
    const colors = categories.map((_, index) => backgroundColor[index])

    const conf = {
        labels: categories,
        datasets: [
            {
                label: 'Usuarios',
                data: values,
                backgroundColor: colors,
                borderColor: 'rgb(82,105,128)',
                borderWidth: 1.5,
            },

        ],
    };
    const pieChartOptions = {
        ...options, onClick:
            (event, elements) => {
                if (elements.length > 0 
                    && filters.gender !== categories[elements[0].index]) {
                    console.log('gender' + categories[elements[0].index])
                    setFilters({ gender: categories[elements[0].index] });

                }
            }
    }
    return <Pie data={conf} options={pieChartOptions} />;
}
PieChart.propTypes = {
    data: PropTypes.object.isRequired,
    setFilters: PropTypes.func.isRequired,
    filters: PropTypes.object.isRequired,
};