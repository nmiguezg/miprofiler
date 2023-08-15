var spinner = document.getElementById('spinner')
// Datos de ejemplo
var data = [
    { categoria: "A", valor: 10 },
    { categoria: "B", valor: 25 },
    { categoria: "C", valor: 15 },
    { categoria: "D", valor: 30 }
];

// Tamaño del gráfico
var width = 200;
var height = 300;

// Crear el contenedor SVG
var svg = d3.select("#chart")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Escala de ejes
var xScale = d3.scaleBand()
    .domain(data.map(d => d.categoria))
    .range([0, width])
    .padding(0.1);

var yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.valor)])
    .range([height, 0]);

// Crear las barras
svg.selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", d => xScale(d.categoria))
    .attr("y", d => yScale(d.valor))
    .attr("width", xScale.bandwidth())
    .attr("height", d => height - yScale(d.valor))
    .attr("fill", "steelblue");

// Agregar ejes
svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale));

svg.append("g")
    .call(d3.axisLeft(yScale));

function startSpinner(){
    spinner.classList.remove('hidden');
    spinner.removeAttribute('hidden');
}
function stopSpinner(){
    spinner.classList.add('hidden');
    spinner.setAttribute('hidden','True');
}
function handleErrors(response) {
    if (response.status != 200) {
        throw Error('Bad username or password');
    }
    return response.json();
}
document.querySelector("form#profiler-form").addEventListener('submit', function (event) {
    event.preventDefault();
    var formulario = event.target; // Accede al formulario que generó el evento
    startSpinner();

    formData = new FormData()
    formData.append('file', formulario.elements['file'].files[0])
    formData.append('algoritmo', formulario.elements['algoritmo'].value)
    fetch('http://localhost:8000/profile',{
          method: 'POST',
          body: formData
    })
    .then(handleErrors)
    .then(response =>
        {
            console.log(Response)
            stopSpinner()
        })
});