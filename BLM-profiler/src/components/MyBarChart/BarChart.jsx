import { useState } from "react"
import "./BarChart.css"

export default function BarChart({ width: chartWidth, height: chartHeight, data, space = chartWidth / 50 }) {
    const categories = Object.keys(data)
    const values = Object.values(data)
    const suma = values.reduce((acum, current) => acum + current, 0)
    const barWidth = chartWidth / categories.length - space
    const labelsSize = chartWidth / 20
    const maxValue = Math.max(...values)
    const xScale = (index) => index * (barWidth + space);
    const yScale = (value) => chartHeight - (value * chartHeight) / maxValue;

    const [tooltip, setTooltip] = useState(null)
    const [tooltipPosition, setTooltipPosition] = useState({ left: 0, top: 0 });

    return (
        <div>
            <svg width={chartWidth - 0 + space} height={chartHeight - 0 + labelsSize}>
                {categories.map((category, index) => {
                    const x = index * (chartWidth / categories.length) + space
                    const h = Math.max(values[index] / suma * chartHeight, Math.max(2, chartHeight / 100))
                    const y = chartHeight - h
                    return (
                        <rect key={index} x={x} y={y} width={barWidth} height={h}
                            fill="steelblue"
                            onMouseEnter={() => setTooltip(category)}
                            onMouseMove={(e) => setTooltipPosition({ left: e.clientX, top: e.clientY })}
                            onMouseLeave={() => {
                                setTooltip(null);
                                setTooltipPosition({ left: 0, top: 0 });
                            }}
                        >
                        </rect>)
                })}
                <g transform={`translate(0, ${chartHeight})`}>
                    {categories.map((category, index) => {
                        return <text key={index} x={xScale(index) + barWidth / 2} y={labelsSize} textAnchor="middle" fontSize={labelsSize+"px"} fill="white">
                            {category}
                        </text>
                    })}
                </g>
                <line x1="0" x2={chartWidth} y1={chartHeight} y2={chartHeight} stroke="white" />
                <line x1="0" x2="0" y1="0" y2={chartHeight} stroke="white" />
            </svg>
            {tooltip && (
                <div
                    className="tooltip"
                    style={{
                        left: tooltipPosition.left + 10, // Ajusta el desplazamiento horizontal
                        top: tooltipPosition.top + 10,   // Ajusta el desplazamiento vertical
                        display: "block",
                    }}
                >
                    {data[tooltip]}
                </div>
            )}
        </div >
    )
}

// function Rect({x}){

// }