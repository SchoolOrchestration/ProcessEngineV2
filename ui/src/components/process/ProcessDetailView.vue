<template>
<section>
  <v-card>
    <v-card-title >
      {{process.definition.name}}
      <v-spacer></v-spacer>
      <v-btn flat><v-icon class='mr-2' >replay</v-icon> Replay</v-btn>
    </v-card-title>
  </v-card>

  <v-expansion-panel popout dark class='mt-3' >
    <v-expansion-panel-content v-for='task in process.task_set' :key='task.id' >
        <v-list-tile slot='header' >
          <v-list-tile-action-text>
            <v-avatar :size='32' color="teal" class='ma-1'>
              <span class="white--text headline">{{task.status}}</span>
            </v-avatar>
          </v-list-tile-action-text>
          <v-list-tile-content>
            <v-list-tile-title>{{task.name}}. {{task.service}}.{{task.method_name}}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

      <v-card>
        <v-card-text>
          <v-subheader>Data</v-subheader>
          <code class='block pa-2' >{{task.payload}}</code>

          <v-subheader>Result</v-subheader>
          <code v-for='result in task.result_set' :key='result.id' class='block pa-2' >
            {{result.response}}
          </code>
        </v-card-text>
      </v-card>
    </v-expansion-panel-content>
  </v-expansion-panel>
</section>
</template>

<script>
export default {
  name: 'ProcessDetailView',
  props: {
    process: { type: Object, required: true }
  }
}
</script>

<style>

</style>
