<template>
<v-list-tile
  @click='$emit("selected", process)'
  :key='process.id' >
  <v-list-tile-avatar>
    <v-icon v-if='isSuccessful' color='green' >check</v-icon>
    <v-icon v-else  color='red' >warning</v-icon>
  </v-list-tile-avatar>
  <v-list-tile-content>
    <v-list-tile-title >{{process.definition.name}}</v-list-tile-title>
    <v-list-tile-sub-title>{{createdDate}}</v-list-tile-sub-title>
  </v-list-tile-content>
  <v-list-tile-action-text >
    {{successfullTasks.length}}/{{unsuccessfullTasks.length}}
  </v-list-tile-action-text>
</v-list-tile>
</template>

<script>
import { DateTime } from 'luxon'

export default {
  name: 'ProcessListItem',
  props: {
    process: {type: Object, required: true}
  },
  computed: {
    successfullTasks () {
      return this.process.task_set.filter((item) => {
        return item.status === 'C'
      })
    },
    unsuccessfullTasks () {
      return this.process.task_set.filter((item) => {
        return item.status !== 'C'
      })
    },
    isSuccessful () {
      return this.successfullTasks.length === this.process.task_set.length
    },
    createdDate () {
      return DateTime
        .fromISO(this.process.created_date)
        .toLocaleString(DateTime.DATETIME_MED)
    }
  }
}
</script>

<style>

</style>
