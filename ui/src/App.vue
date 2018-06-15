<template>
<v-app>
  <!-- <v-navigation-drawer app></v-navigation-drawer> -->
  <v-toolbar color='primary' app dark dense flat>
    <v-toolbar-title>Process Engine</v-toolbar-title>
    <v-toolbar-items class="ml-4 hidden-sm-and-down">
      <v-btn v-for='(item, i) in items' :key='i' :to='item.to' flat>{{item.title}}</v-btn>
    </v-toolbar-items>
  </v-toolbar>
  <v-content>
    <v-container >
      <router-view></router-view>
    </v-container>
  </v-content>
  <v-footer app></v-footer>
</v-app>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      items: [
        { title: 'Processes', to: '/processes' },
        { title: 'Registered Tasks', to: '/tasks' },
        { title: 'Discover Tasks', to: '/discover' },
        { title: 'Monitor', to: '/monitor' }
      ]
    }
  }
}
</script>
