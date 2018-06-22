<template>
  <v-form v-model='isValid' >
    <v-card>
      <v-card-text >
        <v-text-field solo
          label='Payload'
          :rules="[validateJSON]"
          multi-line v-model='payload' >
        </v-text-field>
        <v-subheader>Result</v-subheader>
        <pre>{{result.data}}</pre>
      </v-card-text>
      <!-- <pre>
let url = 'http://localhost:8000'
let data = {{payload}}
axios.post({url, data})
      </pre> -->
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click='create' :disabled="!isValid" >Run</v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RunProcess',
  props: {
    processTemplate: {type: Object}
  },
  data () {
    return {
      isValid: false,
      payload: '',
      result: {}
    }
  },
  mounted () {
    this.setValuesFromTemplate()
  },
  watch: {
    processTemplate () {
      this.setValuesFromTemplate()
    }
  },
  methods: {
    validateJSON (v) {
      try {
        JSON.parse(v)
      } catch (e) {
        return 'Not Valid JSON'
      }
      return true
    },
    setValuesFromTemplate () {
      if (this.processTemplate && this.processTemplate.example_payload) {
        this.payload = JSON.stringify(this.processTemplate.example_payload)
      }
    },
    async create () {
      let url = 'http://localhost:8000/process/'
      let data = {
        template: this.processTemplate.slug,
        payload: this.payload
      }
      let method = 'post'
      this.result = await axios({url, data, method})
    }
  }
}
</script>

<style>

</style>
