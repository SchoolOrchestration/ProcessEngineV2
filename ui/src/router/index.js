import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/pages/Home'
import ProcessPage from '@/components/pages/Processes'
import CreateProcessPage from '@/components/process/CreateProcess'
import RegisteredTasks from '@/components/pages/RegisteredTasks'
import Discover from '@/components/pages/Discover'
import Monitor from '@/components/pages/Monitor'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomePage
    },
    {
      path: '/processes',
      name: 'ProcessPage',
      component: ProcessPage
    },
    {
      path: '/processes/new',
      name: 'CreateProcessPage',
      component: CreateProcessPage
    },
    {
      path: '/tasks',
      name: 'RegisteredTasks',
      component: RegisteredTasks
    },
    {
      path: '/discover',
      name: 'Discover',
      component: Discover
    },
    {
      path: '/monitor',
      name: 'Monitor',
      component: Monitor
    }
  ]
})
