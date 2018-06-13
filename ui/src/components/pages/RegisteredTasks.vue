<template>
  <v-container>
    <v-layout>
      <v-flex>
        <h1 class='headline mx-4' >Registered Tasks</h1>
        <blockquote class='blockquote' >
          Registered tasks are tasks that this process engine knows about.
          Registered tasks can be combined to make up a process
        </blockquote>
      </v-flex>
    </v-layout>
    <v-divider class = 'my-3' ></v-divider>
    <v-layout row wrap>
      <v-flex xs6 v-for='task in tasks' :key='task.id' >
        <v-card class='ma-2' >
          <v-card-title>
            <h2 class='subheading' >{{task.friendly_name}}</h2>
            <v-spacer></v-spacer>
            <v-chip label small >{{task.production_status}}</v-chip>
          </v-card-title>
          <v-card-text>
            <pre>{{task.service}}.{{task.name}}</pre>
            <v-divider class='my-2' ></v-divider>
            <blockquote class='blockquote pa-0 mt-2' >{{task.docs}}</blockquote>
            <v-subheader>Example input</v-subheader>
            <code class='block pa-2' >{{task.example_payload}}</code>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Processes',
  data () {
    return {
      processEngineUrl: 'http://localhost:8000',
      tasks: []
    }
  },
  mounted () {
    this.get()
  },
  methods: {
    async get () {
      let response = await axios.get(`${this.processEngineUrl}/registered-tasks/`)
      this.tasks = response.data
    }
  }
}
</script>

<style>
.block {
  display:block;
}
code {
  background: black;
  color: white;
}
</style>
