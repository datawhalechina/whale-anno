import Vue from 'vue'
import App from './App'
import router from './router'
import { Button, Select, Menu, MenuItem } from 'element-ui'

Vue.config.productionTip = false

Vue.use(Button)
Vue.use(Select)
Vue.use(Menu)
Vue.use(MenuItem)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
