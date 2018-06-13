<template>
<v-container>
  <v-layout>
    <v-flex>
      <h1 class='headline mx-4' >Discover available tasks</h1>
      <blockquote class='blockquote' >
        Find tasks provided by microservices in the network
      </blockquote>
    </v-flex>
  </v-layout>
  <v-layout>
      <v-toolbar >
        <v-toolbar-title>Find available tasks</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-select :items='items' label='Choose a service' ></v-select>
        <!-- <v-text-field label='Search' >
        </v-text-field> -->
      </v-toolbar>
    </v-layout>
</v-container>
</template>

<script>
export default {
  name: 'Discover',
  data () {
    return {
      items: [
        'localhost'
      ]
    }
  }
}
</script>

<style>

</style>
