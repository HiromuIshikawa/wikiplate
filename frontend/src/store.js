import axios from 'axios'
const apiEndpoint = 'https://wikiplate.herokuapp.com/api'

const state = {
  template: {
    infobox: {
      title: '',
      arg: [],
      url: ''
    },
    sections: [],
    wiki: ''
  },
  similars: [],
  loading: false,
  message: ''
}

const actions = {
  async getTemplate (keywords) {
    state.loading = true
    const resTemplate = await axios.get(apiEndpoint + '/template', {
      params: {
        keywords: keywords
      }
    }).catch(() => { console.log('template error') })
    if (resTemplate.data.result === 'Success') {
      state.message = ''
      const resSimilars = await axios.get(apiEndpoint + '/similars').catch(() => { console.log('similars error') })
      const template = resTemplate.data
      const similars = resSimilars.data.similars
      for (var i = 0, len = similars.length; i < len; ++i) {
        if (similars[i].ib_title === template.infobox.title) {
          similars[i]._rowVariant = 'success'
        } else {
          similars[i]._rowVariant = ''
        }
      }
      state.template = Object.assign({}, template)
      state.similars = Object.assign([], similars)
    } else {
      state.message = '類似記事が抽出できませんでした．'
      state.template = {
        infobox: {
          title: '',
          arg: [],
          url: ''
        },
        sections: [],
        wiki: ''
      }
      state.similars = []
    }
    state.loading = false
  },
  async regenerateTemplate (infobox) {
    state.loading = true
    const resTemplate = await axios.get(apiEndpoint + '/regenerate', {
      params: {
        infobox: infobox
      }
    }).catch(() => { console.log('template error') })
    if (resTemplate.data.result === 'Success') {
      state.message = ''
      const template = resTemplate.data
      for (var i = 0, len = state.similars.length; i < len; ++i) {
        if (state.similars[i].ib_title === template.infobox.title) {
          state.similars[i]._rowVariant = 'success'
        } else {
          state.similars[i]._rowVariant = ''
        }
      }
      state.template = Object.assign({}, template)
    } else {
      state.message = '記事テンプレート生成に失敗しました．'
      state.template = {
        infobox: {
          title: '',
          arg: [],
          url: ''
        },
        sections: [],
        wiki: ''
      }
    }
    state.loading = false
  }
}

export default {
  state,
  actions
}
