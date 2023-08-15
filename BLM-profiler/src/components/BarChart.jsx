export default function BarChart({ width, height, categories, values }) {

    return (
        <svg width={width} height={height}>
            {categories.map((value, index) => {
                return <rect x={index * 53} y={height - value} width="43" height={value} fill="steelblue" />
            })}
            <rect x="53." y="49." width="43." height="250" fill="steelblue"></rect>
        </svg>
    )
}
// function Rect({x}){

// }