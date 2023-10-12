function handleErrors(response) {
    if (!response.ok) {
        throw Error("ProfileServiceError: " + response.statusText);
    }
    return response.json();
}

export default class ProfilerService {
    constructor() {
        throw new Error("Cannot instantiate abstract class");
    }

    static endpoint = "/api/profiler";

    static async profileUsers(file, algorithm) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('algoritmo', algorithm);
        return fetch(`${this.endpoint}/profile`, {
            method: 'POST',
            body: formData
        })
            .then(handleErrors)
            .then(this.#processColl)
            .catch(error => { throw error });
    }
    static async findCollections() {
        return fetch(`${this.endpoint}/collections`)
            .then(handleErrors)
            .then(collList => {
                return collList?.map(coll => {return this.#processColl(coll)})
            })
            .catch(error => { throw error });
    }
    static async getCollectionById(coll_id) {
        return fetch(`${this.endpoint}/collections/${coll_id}`)
            .then(handleErrors)
            .then(this.#processColl)
            .catch(error => { throw error });
    }

    static async findUsers(coll_id, limit = 100, offset = 0, filters = {}) {

        const queryParams = new URLSearchParams({
            limit: limit,
            offset: offset,
            ...this.#formatFilters(filters)
        });

        return fetch(`${this.endpoint}/collections/${coll_id}/users?${queryParams}`)
            .then(handleErrors)
            .then(data => {
                if (data.length == 0) {
                    return null
                }
                return data?.map(d => ({
                    id: d.id,
                    genero: d.gender[0] == 'M' ? 'Masculino' : 'Femenino',
                    edad: d.age.toLocaleLowerCase() == '50-xx' ? '50+' : d.age,
                    posts: d.posts,
                }))
            })
            .catch(error => { throw error });
    }
    static async getUsersStats(coll_id, filters = {}) {
        const queryParams = new URLSearchParams({
            ...this.#formatFilters(filters)
        });

        return fetch(`${this.endpoint}/collections/${coll_id}/stats?${queryParams}`)
            .then(handleErrors)
            .then(this.#getUsersStats)
            .catch(error => { throw error });
    }
    static #processColl = data => {
        return {
            id: data.id,
            name: data.nombre,
            algorithm: data.algoritmo,
            timestamp: data.fecha_creacion,
            time: data.tiempo,
            users: this.#getUsersStats(data.users_stats),
        }
    }
    static #formatFilters = filters => {
        const filtersTd = {}
        if (filters.age && filters.age == '50+') {
            filtersTd.age = '50-XX'
        }
        if (filters.gender) {
            filtersTd.gender = filters.gender == 'Masculino' ? 'MALE' : 'FEMALE'
        }
        return filtersTd;
    }
    static #getUsersStats = users_stats => {
        {
            return {
                'totalUsers': users_stats.total_users,
                'age': {
                    '18-24': users_stats['age']['18-24'],
                    '25-34': users_stats['age']['25-34'],
                    '35-49': users_stats['age']['35-49'],
                    '+50': users_stats['age']['50-XX'],
                },
                'gender': {
                    'Masculino': users_stats['gender']['MALE'],
                    'Femenino': users_stats['gender']['FEMALE'],
                }
            }
        }

    }
}
