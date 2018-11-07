import Vue from 'vue'
import Router from 'vue-router'
import TemplateEditor from '@/components/TemplateEditor'
import SimilarsList from '@/components/SimilarsList'

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
    }
  ]
})
