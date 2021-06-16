import Vue from 'vue'
import Router from 'vue-router'
import NER from '@/components/NER'
import home from '@/components/home'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'NER',
      component: NER,
      props: {
        entityTypes: true
      }
    },
    {
      path: '/home',
      name: 'home',
      component: home,
      props: true
    }
  ]
})
