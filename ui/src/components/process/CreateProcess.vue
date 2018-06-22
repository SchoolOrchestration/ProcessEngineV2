<template>
  <v-form>
    <v-card>
      <v-card-text>
        <h2 class='subheading' >(WIP) Create a new process</h2>
      </v-card-text>
      <v-card-text>
        <v-text-field
          v-for='field in fields'
          :key='field.key'
          v-model='process[field.key]'
          v-bind='field' >
        </v-text-field>
      </v-card-text>
    </v-card>
  </v-form>
</template>

<script>
export default {
  name: 'CreateProcess',
  data () {
    return {
      process: {},
      fields: [
        {
          key: 'name',
          label: 'Name'
        },
        {
          key: 'version',
          label: 'Version',
          hint: 'e.g.: 0.1, 1.0 etc'
        },
        {
          key: 'docs',
          label: 'Docs',
          multiLine: true
        },
        {
          key: 'example_payload',
          label: 'Example payload',
          multiLine: true
        },
        {
          key: 'example_response',
          label: 'Example response',
          multiLine: true
        }
      ]
    }
  }
}
</script>

<style>

</style>
