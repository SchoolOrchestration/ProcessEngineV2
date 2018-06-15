<template>
  <v-layout>
    <v-flex xs3>
      <v-list dense >
        <v-subheader>Processes</v-subheader>
        <template v-for='process in processes' >
        <process-list-item
          @selected='setProcess'
          :process='process'
          :key='process.id' ></process-list-item>
        <v-divider :key='`d-${process.id}`' ></v-divider>
        </template>
      </v-list>
    </v-flex>
    <v-flex xs9>
      <process-detail-view class='ma-4'
        v-if='activeProcess'
        :process='activeProcess' >
      </process-detail-view>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios'
import ProcessListItem from '../process/ProcessListItem'
import ProcessDetailView from '../process/ProcessDetailView'

export default {
  name: 'Monitor',
  components: {ProcessListItem, ProcessDetailView},
  data () {
    return {
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
      let response = await axios.get(`${this.processEngineUrl}/process/`)
      this.processes = response.data
    },
    setProcess (process) {
      this.activeProcess = process
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
  max-height: 300px;
  overflow: auto;
}
</style>
