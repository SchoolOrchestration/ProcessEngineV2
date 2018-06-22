<template>
  <v-container>
    <v-layout>
      <v-flex>
        <h1 class='headline ma-2' >Defined Processes</h1>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex xs4>
        <v-list class='elevation-4 ma-2 pb-0' >
          <v-list-tile
            @click='activeProcess = process'
            v-for='process in processes'
            :key='process.id' >
            <v-list-tile-content>
              <v-list-tile-title >{{process.name}}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <v-btn flat><v-icon>add</v-icon> Create a process</v-btn>
      </v-flex>
      <v-flex xs8>
        <section v-if='activeProcess' >
        <v-card class='ma-2' >
          <v-card-title >
            <h1 class='subheading ma-2' >{{activeProcess.name}}</h1>
            <v-spacer></v-spacer>
            <v-btn @click='createProcessDialog=true' small color='primary' ><v-icon >play_arrow</v-icon> Run</v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <blockquote class='blockquote pa-2' >{{activeProcess.docs}}</blockquote>
            <v-subheader>Example Request</v-subheader>
            <code class='block pa-2'>
url = '{{processEngineUrl}}/process/'
data = {
  name: '{{activeProcess.slug}}',
  payload: {{activeProcess.example_payload}}
}
result = requests.post(url, data)
            </code>
            <v-subheader>Example Response</v-subheader>
            <code class='block pa-2'>{{activeProcess.example_response}}</code>
          </v-card-text>
        </v-card>

        <h1 class='subheading ma-2' >Tasks</h1>

        <v-card v-if='activeProcess'
          v-for='task in activeProcess.tasks' :key='task.id'
          class='ma-2 mt-0' >
          <v-card-title >
            <h1 class='subheading ma-2' >
              {{task.name}}.
            </h1>
            <v-spacer></v-spacer>
            <v-btn @click='vue.set(task, "showDetails", false)' v-show='task.showDetails === true' icon small ><v-icon>expand_less</v-icon></v-btn>
            <v-btn @click='vue.set(task, "showDetails", true)'  v-show='!task.showDetails' icon small ><v-icon>expand_more</v-icon></v-btn>
          </v-card-title>
          <v-card-text v-show='task.showDetails' >
            <v-subheader>Execution details</v-subheader>
            <section class='mx-3' >
              <div><strong>Runner:</strong> {{task.runner}}</div>
              <div>
                <strong>Schedule:</strong>
                <span v-if='task.run_immediately' >
                  Run immediately
                </span>
                <span v-else-if='task.schedule_offset_from_field.length == 2' >
                  Run: {{task.schedule_offset_from_field}} after the
                </span>
                <span v-else >
                  Run: {{task.schedule_offset_from_now}} mins after creation
                </span>
              </div>

              <div v-if='task.is_async' >
                Runs asyncronously.
                Task will be run in the background.
                You can poll the process for progress updates
              </div>
              <div v-if='task.is_async' >
                Runs syncronously.
                Response will be returned with initial query
              </div>
            </section>

            <v-subheader>Payload template</v-subheader>
            <p class='ma-2' >The template shows how the payload data from the process above is mapped into data passed to the task</p>
            <code class='block ma-2' >{{task.payload_template}}</code>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions >
            <v-spacer></v-spacer>
            <code>{{task.registered_task.service}}:{{task.registered_task.method_to_call}}</code>
          </v-card-actions>
        </v-card>
        </section>

      </v-flex>
    </v-layout>
    <v-dialog v-model='createProcessDialog' width=500 >
      <v-card>
        <run-process :process-template='activeProcess' ></run-process>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import vue from 'Vue'
import axios from 'axios'
import RunProcess from '@/components/process/RunProcess'
export default {
  name: 'Processes',
  components: {RunProcess},
  data () {
    return {
      vue: vue,
      createProcessDialog: false,
      processEngineUrl: 'http://localhost:8000',
      processes: [],
      activeProcess: null
    }
  },
  mounted () {
    this.get()
  },
  methods: {
    async get () {
      let response = await axios.get(`${this.processEngineUrl}/process-definitions/`)
      this.processes = response.data
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
