import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import ProcessPage from '@/components/pages/Processes'
import RegisteredTasks from '@/components/pages/RegisteredTasks'
import Discover from '@/components/pages/Discover'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/processes',
      name: 'ProcessPage',
      component: ProcessPage
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
    }
  ]
})
