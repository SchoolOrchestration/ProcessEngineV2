<template>
  <v-container>
    <v-layout row >
      <v-flex>
        <v-list>
          <v-subheader>Recent processes</v-subheader>
          <template v-for='process in processes' >
            <v-list-tile
              @click='activeProcess = process'
              :key='process.id' >
              <v-list-tile-avatar>
                <v-progress-circular v-if='completeAsPercent(process) < 100' color='amber' :value='completeAsPercent(process)' ></v-progress-circular>
                <v-icon v-else color='green' dark >check_circle</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title >
                  #{{process.id}}:
                  {{process.definition.name}}</v-list-tile-title>
                <v-list-tile-sub-title >
                  Created: {{datetimeformat(process.created_date)}}
                </v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action-text>
                {{ getCompleteTasks(process).length }} / {{process.task_set.length}}
              </v-list-tile-action-text>
            </v-list-tile>
          </template>
        </v-list>
      </v-flex>
      <v-flex>
        <v-list>
          <v-subheader>Tasks</v-subheader>
          <template v-if='activeProcess && activeProcess.task_set'
            v-for='task in activeProcess.task_set' >
            <v-list-tile @click='activeTask = task' :key='task.id' >
              <v-list-tile-avatar :color='getStatusColor(task.status)'  >
                  <span class="white--text headline">{{task.status}}</span>

              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title >
                  #{{task.id}}: {{task.service}}.{{task.method_name}}
                </v-list-tile-title>
                <v-list-tile-sub-title >
                  Schedule: {{datetimeformat(task.scheduled_datetime)}}
                </v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </template>
        </v-list>
      </v-flex>
      <v-flex>
        <v-card class='ma-2' v-if='activeTask'>
          <v-card-title>
            <v-subheader>Task details</v-subheader>
          </v-card-title>
          <v-card-text>
            <code class='block' >{{activeTask}}</code>
          </v-card-text>
          <v-card-actions >
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>

</template>

<script>
import axios from 'axios'
export default {
  name: 'HomePage',
  mounted () {
    this.getProcesses()
  },
  data () {
    return {
      processes: [],
      activeProcess: {},
      activeTask: {}
    }
  },
  methods: {
    async getProcesses () {
      let result = await axios.get('http://localhost:8000/process/')
      this.processes = result.data
    },
    completeAsPercent (process) {
      return (this.getCompleteTasks(process).length / process.task_set.length) * 100
    },
    getCompleteTasks (process) {
      return process.task_set.filter((task) => {
        return (task.status === 'C')
      })
    },
    getStatusColor (status) {
      if (['C'].indexOf(status) !== -1) {
        return 'green'
      }
      if (['F', 'X'].indexOf(status) !== -1) {
        return 'red'
      }
      return 'grey'
    }
  }
}
</script>

<style>

</style>
