function handleErrors(response) {
    if (!response.ok) {
        throw Error("ProfileServiceError: " + response.statusText);
    }
    return response.json();
}

export default class ProfileService {
    constructor() {
        throw new Error("Cannot instantiate abstract class");
    }

    static endpoint = "/api";

    static async profileUsers(file, algorithm) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('algoritmo', algorithm);
        return fetch(`${this.endpoint}/profile`, {
            method: 'POST',
            body: formData
        })
            .then(handleErrors)
            .then(data => {
                const res = {}
                res['usuarios'] = data?.map(d => ({
                    id: d.label,
                    genero: d.gender[0] == 'M' ? 'Masculino' : 'Femenino',
                    edad: d.age.toLowerCase() == '50-xx' ? '50+' : d.age,
                    posts: d.post
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
    static async getUsers(limit=100, offset=0) {
        return fetch(`${this.endpoint}/users?limit=${limit}&offset=${offset}`)
            .then(handleErrors)
            .then(data => {
                if (data.Users.length == 0) {
                    return null
                }
                const res = {}
                res['usuarios'] = data.Users?.map(d => ({
                    id: d.label,
                    genero: d.gender[0] == 'M' ? 'Masculino' : 'Femenino',
                    edad: d.age.toLocaleLowerCase() == '50-xx' ? '50+' : d.age,
                    posts: d.post,
                    timestamp: d.date,
                    collection: d.collection
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
                }
                res['usuarios'].forEach(u => {
                    res['grupos']['edad'][u.edad] += 1
                    res['grupos']['genero'][u.genero] += 1
                })
                return res
            }
            ).catch(error => { throw error });
    }
}
