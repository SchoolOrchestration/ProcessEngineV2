import axios from 'axios'

export default {
  methods: {
    $api () {
      let baseUrl = 'http://localhost:8000'
      let vm = this
      return {
        services: {
          async list () {
            let response = await axios.get(`${baseUrl}/registered-services/`)
            vm.services = response.data
          }
        }
      }
      // return {
      //   async list () {
      //     let response = await axios.get(`${this.baseUrl}/registeted-service/`)
      //     return response.data
      //   }
      // }
    }
  }
}
