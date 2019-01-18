import Vue from 'vue'
import Router from 'vue-router'
import TemplateEditor from '@/components/TemplateEditor'
import SimilarsList from '@/components/SimilarsList'
import About from '@/components/About'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Template',
      component: TemplateEditor
    },
    {
      path: '/similars',
      name: 'Similars',
      component: SimilarsList
    },
    {
      path: '/about',
      name: 'About',
      component: About
    }
  ]
})
