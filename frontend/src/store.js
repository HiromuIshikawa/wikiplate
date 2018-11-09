import axios from 'axios'
const apiEndpoint = 'http://localhost:5000/api'

const state = {
  template: {
    title: '',
    infobox: {
      title: '',
      infobox: '',
      arg: [],
      url: ''
    },
    sections: [],
    wiki: ''
  },
  similars: [],
  loading: false
}

const actions = {
  async getTemplate (title, keywords) {
    // TODO: Get Tempalate from Flask server
    state.loading = true
    const resTemplate = await axios.get(apiEndpoint + '/template', {
      params: {
        title: title,
        keywords: keywords
      }
    }).catch(() => { console.log('template error') })
    const resSimilars = await axios.get(apiEndpoint + '/similars').catch(() => { console.log('similars error') })
    const template = resTemplate.data
    const similars = resSimilars.data.similars

    state.template = Object.assign({}, template)
    state.similars = Object.assign([], similars)
    state.loading = false
  }
}

export default {
  state,
  actions
}
