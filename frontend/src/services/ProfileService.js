function handleErrors(response) {
    if (!response.ok) {
        throw Error("ProfileServiceError: " + response.statusText);
    }
    return response.json();
}
// function validateCSVFile(file) {
//     //sync function that opens the file and asserts that has a column named 'label', and a column named 'post'
//     return new Promise((resolve, reject) => {
//         const reader = new FileReader();
//         reader.onload = function (e) {
//             const csv = e.target.result.split('\n');
//             const header = csv[0].split(',');
//             if (header.includes('label') && header.includes('post')) {
//                 resolve(true);
//             } else {
//                 reject('El archivo no tiene las columnas requeridas (label, post)');
//             }
//         };
//         reader.readAsText(file);
//     });
// }

export default class ProfileService {
    constructor() {
        throw new Error("Cannot instantiate abstract class");
    }

    static endpoint = "/api";

    static async profileUsers(file, algorithm) {
        const formData = new FormData();
        // validateCSVFile(file).then(() => {}, () => { throw Error("File not valid: file must have two columns named label and post.") });
        formData.append('collection', file);
        formData.append('algoritmo', algorithm);
        return fetch(`${this.endpoint}/profile`, {
            method: 'POST',
            body: formData
        })
            .then(handleErrors)
            .then(data => {
                const res = {}
                res['usuarios'] = data.Users?.map(d => ({
                    id: d.user,
                    genero: d.gender[0] == 'M' ? 'Masculino' : 'Femenino',
                    edad: d.age == '50-xx' ? '50+' : d.age
                })
                )
                res['grupos'] = {
                    edad: {
                        '18-24': 0,
                        '25-34': 0,
                        '35-49': 0,
                        '50+': 0
                    },
                    genero: {
                        'Masculino': 0,
                        'Femenino': 0
                    },
                    algoritmo: algorithm
                }
                res['usuarios'].forEach(u => {
                    res['grupos']['edad'][u.edad] += 1
                    res['grupos']['genero'][u.genero] += 1
                })
                return res

            }).catch(error => { throw error });
    }
}
